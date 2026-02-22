import os
import torch
import datetime
from collections import OrderedDict
from typing import List, Dict, Tuple


def load_checkpoint(path: str) -> dict:
    """Load checkpoint from .pth file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model not found: {path}")
    cpt = torch.load(path, map_location="cpu")
    print(f"Loaded: {os.path.basename(path)} (SR: {cpt.get('sr')}, v: {cpt.get('version')})")
    return cpt

def extract_weights(cpt: dict) -> OrderedDict:
    """Extract weights from checkpoint (filters enc_q)."""
    weights = cpt.get("model") or cpt.get("weight")
    if weights is None:
        raise ValueError("Unknown checkpoint format")
    return OrderedDict((k, v) for k, v in weights.items() if "enc_q" not in k)

def compute_all_differences(
    cpt_a: dict,
    cpt_b: dict,
    modules: List[str] = None
) -> Tuple[Dict[str, torch.Tensor], Dict[str, dict]]:
    """
    Compute weight differences between two models at the element level.

    Returns:
        diff_tensors: Dict {layer_name: abs_diff_tensor}
        stats: Dict {layer_name: {"mean", "max", "numel", "shape"}}
    """
    w_a = extract_weights(cpt_a)
    w_b = extract_weights(cpt_b)

    diff_tensors = {}
    stats = {}

    for key in w_a.keys():
        # Module filter
        if modules is not None:
            if not any(m in key for m in modules) and "bias" not in key:
                continue

        if key not in w_b:
            continue

        a = w_a[key].float()
        b = w_b[key].float()

        if a.shape != b.shape:
            continue

        diff = (a - b).abs()
        diff_tensors[key] = diff

        stats[key] = {
            "mean": diff.mean().item(),
            "max": diff.max().item(),
            "numel": a.numel(),
            "shape": list(a.shape)
        }

    return diff_tensors, stats


def compute_threshold(diff_tensors: Dict[str, torch.Tensor], ratio: float) -> float:
    """
    Compute threshold for selecting TOP ratio% weights.
    """
    # Concatenate all differences into one vector
    all_diffs = torch.cat([d.flatten() for d in diff_tensors.values()])
    total = all_diffs.numel()

    # Number of weights to select
    k = int(total * ratio)
    k = max(1, min(k, total))  # At least 1, max all

    # Find the k-th largest element (threshold)
    threshold = torch.kthvalue(all_diffs, total - k + 1).values.item()

    print(f"Total parameters: {total:,}")
    print(f"Ratio: {ratio} -> selecting {k:,} weights ({100*ratio:.2f}%)")
    print(f"Threshold: {threshold:.8f}")

    return threshold


def create_copy_masks(
    diff_tensors: Dict[str, torch.Tensor],
    threshold: float
) -> Tuple[Dict[str, torch.Tensor], Dict[str, int]]:
    """
    Create binary masks for weight blending.

    Returns:
        masks: Dict {layer_name: bool_tensor} where True = blend
        counts: Dict {layer_name: number_of_selected_elements}
    """
    masks = {}
    counts = {}

    for key, diff in diff_tensors.items():
        mask = diff >= threshold
        masks[key] = mask
        counts[key] = mask.sum().item()

    total_selected = sum(counts.values())
    print(f"Total selected weights: {total_selected:,}")

    return masks, counts


def create_random_masks(
    weights: OrderedDict,
    ratio: float = 0.5,
    seed: int = None
) -> Tuple[Dict[str, torch.Tensor], Dict[str, int]]:
    """
    Create random binary masks for weight blending.

    Instead of selecting by difference magnitude, randomly selects
    a configurable percentage of weights.

    Args:
        weights: Extracted weights from extract_weights()
        ratio: Fraction of weights to select (0.0 to 1.0)
        seed: Optional seed for reproducibility

    Returns:
        masks: Dict {layer_name: bool_tensor} where True = blend
        counts: Dict {layer_name: number_of_selected_elements}
    """
    if seed is not None:
        torch.manual_seed(seed)

    masks = {}
    counts = {}
    total_params = 0
    total_selected = 0

    for key, tensor in weights.items():
        if "enc_q" in key:
            continue
        mask = torch.rand(tensor.shape) < ratio
        masks[key] = mask
        count = mask.sum().item()
        counts[key] = count
        total_params += tensor.numel()
        total_selected += count

    print(f"Total parameters: {total_params:,}")
    print(f"Randomly selected: {total_selected:,} ({100 * total_selected / total_params:.2f}%)")
    if seed is not None:
        print(f"Seed: {seed}")

    return masks, counts


def apply_mask_blend(
    source_cpt: dict,
    target_cpt: dict,
    masks: Dict[str, torch.Tensor],
    blend_factor: float = 0.5
) -> OrderedDict:
    """
    Blend selected weights (according to masks) from source into target model.

    For selected weights: result = (1 - blend_factor) * target + blend_factor * source
    For unselected weights: result = target
    """
    source_weights = extract_weights(source_cpt)
    target_weights = extract_weights(target_cpt)

    result = OrderedDict()
    blended_total = 0

    for key in target_weights.keys():
        tgt = target_weights[key].float()

        if key in masks and key in source_weights:
            src = source_weights[key].float()
            mask = masks[key]

            if src.shape == tgt.shape:
                blended = (1 - blend_factor) * tgt + blend_factor * src
                result[key] = torch.where(mask, blended, tgt)
                blended_total += mask.sum().item()
            else:
                result[key] = tgt
        else:
            result[key] = tgt

    print(f"Blended {blended_total:,} individual weights (factor={blend_factor})")
    return result


def save_model(weights: OrderedDict, base_cpt: dict, output_path: str, info: str = "") -> str:
    """Save model."""
    opt = OrderedDict()
    opt["weight"] = OrderedDict((k, v.half()) for k, v in weights.items())
    opt["config"] = base_cpt.get("config")
    opt["sr"] = base_cpt.get("sr")
    opt["f0"] = base_cpt.get("f0", 1)
    opt["version"] = base_cpt.get("version", "v2")
    opt["creation_date"] = datetime.datetime.now().isoformat()
    opt["info"] = info

    torch.save(opt, output_path)
    print(f"Saved: {output_path} ({os.path.getsize(output_path) / 1024 / 1024:.2f} MB)")
    return output_path
