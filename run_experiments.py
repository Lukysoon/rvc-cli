import json
import os
import sys
import argparse
import time

import weight_arithmetic as wa
import inference


def run_single_experiment(params, output_dir):
    """Run a single weight arithmetic experiment. Returns stats dict."""
    name = params["name"]
    model_a = params["model_a"]
    model_b = params["model_b"]
    ratio = params["ratio"]
    blend_factor = params["blend_factor"]
    modules = params.get("modules")
    output_path = os.path.join(output_dir, f"{name}.pth")

    # 1. Load blend models
    cpt_a = wa.load_checkpoint(model_a)
    cpt_b = wa.load_checkpoint(model_b)

    # 2. Load reference models for diff computation (or fall back to blend models)
    ref_a = params.get("ref_a")
    ref_b = params.get("ref_b")
    if ref_a and ref_b:
        cpt_ref_a = wa.load_checkpoint(ref_a)
        cpt_ref_b = wa.load_checkpoint(ref_b)
        print(f"  Using reference models for diff map")
    else:
        cpt_ref_a = cpt_a
        cpt_ref_b = cpt_b

    mode = params.get("mode", "threshold")

    if mode == "random":
        # Random mask selection
        seed = params.get("seed")
        print(f"\nCreating random masks (ratio={ratio}, seed={seed})...")
        weights = wa.extract_weights(cpt_a)
        masks, element_counts = wa.create_random_masks(weights, ratio, seed, modules)
        threshold = None
    else:
        # Threshold-based selection using REFERENCE models
        normalization = params.get("normalization")
        print(f"\nComputing weight differences...")
        diff_tensors, stats = wa.compute_all_differences(cpt_ref_a, cpt_ref_b, modules, normalization=normalization)
        
        print(f"Analyzed {len(diff_tensors)} layers")

        print(f"\nComputing threshold for ratio={ratio}...")
        threshold = wa.compute_threshold(diff_tensors, ratio)

        print(f"\nCreating masks...")
        masks, element_counts = wa.create_copy_masks(diff_tensors, threshold)

    # 3b. Write layers log
    layers_log_path = os.path.join(output_dir, f"{name}_layers.txt")
    weights_ref = wa.extract_weights(cpt_ref_a if ref_a else cpt_a)
    with open(layers_log_path, "w") as f:
        f.write(f"Experiment: {name}\n")
        if mode == "random":
            f.write(f"Mode: random (ratio={ratio}, seed={params.get('seed')})\n")
        else:
            f.write(f"Mode: threshold (ratio={ratio}, normalization={params.get('normalization')})\n")
        layers_with_weights = sum(1 for k, c in element_counts.items() if c > 0)
        f.write(f"Layers with copied weights: {layers_with_weights} / {len(element_counts)}\n\n")
        f.write(f"{'Layer':<60} {'Selected':>10} {'Total':>10} {'%':>7}\n")
        f.write("-" * 90 + "\n")
        sorted_counts = sorted(element_counts.items(), key=lambda x: x[1], reverse=True)
        for key, count in sorted_counts:
            if count > 0:
                total = weights_ref[key].numel() if key in weights_ref else masks[key].numel()
                pct = 100 * count / total if total > 0 else 0
                f.write(f"{key:<60} {count:>10,} {total:>10,} {pct:>6.1f}%\n")
    print(f"  Layers log: {layers_log_path}")

    # 4. Blend weights
    print(f"\nBlending weights (factor={blend_factor})...")
    result_weights = wa.apply_mask_blend(cpt_a, cpt_b, masks, blend_factor)

    # 5. Save
    all_weights = wa.extract_weights(cpt_b)
    total_params = sum(w.numel() for w in all_weights.values())
    selected = sum(element_counts.values())

    ref_info = ""
    if ref_a and ref_b:
        ref_info = f" [diff map: {os.path.basename(ref_a)} vs {os.path.basename(ref_b)}]"

    if mode == "random":
        info = (
            f"Randomly blended {ratio*100:.1f}% of weights "
            f"(factor={blend_factor}, seed={params.get('seed')}) from {os.path.basename(model_a)} "
            f"into {os.path.basename(model_b)}{ref_info}"
        )
    else:
        info = (
            f"Blended {ratio*100:.1f}% most different weights "
            f"(factor={blend_factor}) from {os.path.basename(model_a)} "
            f"into {os.path.basename(model_b)}{ref_info}"
        )
    wa.save_model(result_weights, cpt_b, output_path, info)

    return {
        "name": name,
        "output_path": output_path,
        "layers": len(masks),
        "total_params": total_params,
        "selected": selected,
        "threshold": threshold,
    }


def run_experiment_inference(pth_path, input_audio, output_wav, pitch=0):
    """Run inference on a blended model."""
    inference.run_pipeline(
        pitch=pitch,
        input_path=input_audio,
        output_path=output_wav,
        pth_path=pth_path,
    )


def main():
    parser = argparse.ArgumentParser(description="Run weight arithmetic experiments from JSON config")
    parser.add_argument("--config", default="experiments.json", help="Path to JSON config file")
    args = parser.parse_args()

    # Load config
    with open(args.config) as f:
        config = json.load(f)

    output_dir = config.get("output_dir", "experiments_output")
    os.makedirs(output_dir, exist_ok=True)

    defaults = config.get("defaults", {})
    infer_config = config.get("inference", {})
    experiments = config["experiments"]

    print(f"{'='*60}")
    print(f"Running {len(experiments)} experiments")
    print(f"Output directory: {output_dir}")
    print(f"{'='*60}\n")

    results = []
    total_start = time.time()

    for i, exp in enumerate(experiments):
        # Merge defaults with experiment overrides
        params = {**defaults, **exp}

        name = params["name"]
        print(f"\n{'='*60}")
        print(f"[{i+1}/{len(experiments)}] {name}")
        print(f"  model_a: {params['model_a']}")
        print(f"  model_b: {params['model_b']}")
        if params.get("ref_a") and params.get("ref_b"):
            print(f"  ref_a: {params['ref_a']}")
            print(f"  ref_b: {params['ref_b']}")
        print(f"  ratio: {params['ratio']}, blend_factor: {params['blend_factor']}")
        if params.get("mode") == "random":
            print(f"  mode: random, seed: {params.get('seed')}")
        if params.get("modules"):
            print(f"  modules: {params['modules']}")
        print(f"{'='*60}")

        exp_start = time.time()

        # Run blend
        stats = run_single_experiment(params, output_dir)
        stats["duration"] = time.time() - exp_start

        # Run inference
        input_audios = infer_config.get("input_audio", [])
        if isinstance(input_audios, str):
            input_audios = [input_audios]
        if input_audios:
            pitch = infer_config.get("pitch", 0)
            stats["output_wavs"] = []
            for audio_file in input_audios:
                audio_stem = os.path.splitext(os.path.basename(audio_file))[0]
                output_wav = os.path.join(output_dir, f"{name}_{audio_stem}.wav")
                print(f"\nRunning inference: {audio_file} -> {output_wav}")
                run_experiment_inference(stats["output_path"], audio_file, output_wav, pitch)
                stats["output_wavs"].append(output_wav)

        results.append(stats)

    total_duration = time.time() - total_start

    # Summary table
    print(f"\n\n{'='*60}")
    print(f"SUMMARY ({len(results)} experiments in {total_duration:.1f}s)")
    print(f"{'='*60}")
    print(f"{'Name':<25} {'Ratio':>6} {'Selected':>12} {'Threshold':>12} {'Time':>6}")
    print(f"{'-'*25} {'-'*6} {'-'*12} {'-'*12} {'-'*6}")

    for i, (exp, stats) in enumerate(zip(experiments, results)):
        params = {**defaults, **exp}
        pct = 100 * stats["selected"] / stats["total_params"]
        thresh_str = f"{stats['threshold']:.6f}" if stats['threshold'] is not None else "random"
        print(
            f"{stats['name']:<25} "
            f"{params['ratio']:>6.2f} "
            f"{stats['selected']:>9,} ({pct:>4.1f}%) "
            f"  {thresh_str:>12} "
            f"{stats['duration']:>5.1f}s"
        )

    print(f"\nAll outputs saved to: {output_dir}/")


if __name__ == "__main__":
    main()
