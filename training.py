import subprocess
import os

import logging
from custom_logging import get_logger
from pathlib import Path

logging.getLogger("torch").setLevel(logging.ERROR)


def run_command(command, logger):

    try:
        # Use shell=True and create a new shell session
        process = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )

        return True
    except subprocess.CalledProcessError as e:
        logger.info(f"Error executing command: {e}")
        logger.info(f"Error output: {e.stderr}")
        raise Exception(e.stderr)


# Preprocess command
def run_preprocess(model_name, cpu_cores, cut_preprocess, process_effects, noise_reduction, noise_reduction_strength, logger):
    
    sample_rate = 48000
    dataset_path = os.path.join("datasets", model_name)

    logger.info("===PREPROCESS==")
    logger.info(f"model_name {model_name}")
    logger.info(f"dataset_path {dataset_path}")
    logger.info(f"sample_rate {sample_rate}")
    logger.info(f"cpu_cores {cpu_cores}")
    logger.info(f"cut_preprocess {cut_preprocess}")
    logger.info(f"process_effects {process_effects}") 
    logger.info(f"noise_reduction {noise_reduction}")
    logger.info(f"noise_reduction_strength {noise_reduction_strength}")
    logger.info("===============")
    
    cmd = (
        f"venv/bin/python3 rvc_cli.py preprocess "
        f"--model_name {model_name} "
        f"--dataset_path {dataset_path} "
        f"--sample_rate {sample_rate} "
        f"--cpu_cores {cpu_cores} "
        f"--cut_preprocess {cut_preprocess} "
        f"--process_effects {process_effects} "
        f"--noise_reduction {noise_reduction} "
        f"--noise_reduction_strength {noise_reduction_strength} "
    )
    return run_command(cmd, logger)

# Extract command
def run_extract(model_name, cpu_cores, hop_size, logger):

    rvc_version = "v2"
    f0_method = "rmvpe"
    pitch_guidance = True
    gpu = 0
    sample_rate = 48000
    embedder_model = "contentvec"

    logger.info("===EXTRACT FEATURES===")
    logger.info(f"model_name {model_name}")
    logger.info(f"rvc_version {rvc_version}")
    logger.info(f"f0_method {f0_method}")
    logger.info(f"pitch_guidance {pitch_guidance}")
    logger.info(f"hop_length {hop_size}")
    logger.info(f"cpu_cores {cpu_cores}")
    logger.info(f"gpu {gpu}")
    logger.info(f"sample_rate {sample_rate}")
    logger.info(f"embedder_model {embedder_model}")
    logger.info("=====================")

    cmd = (
        f"venv/bin/python3 rvc_cli.py extract "
        f"--model_name {model_name} "
        f"--rvc_version {rvc_version} "
        f"--f0_method {f0_method} "
        f"--pitch_guidance {pitch_guidance} "
        f"--hop_length {hop_size} "
        f"--cpu_cores {cpu_cores} "
        f"--gpu {gpu} "
        f"--sample_rate {sample_rate} "
        f"--embedder_model {embedder_model} "
    )
    return run_command(cmd, logger)

# Train command
def run_train(model_name, save_every_epoch, total_epoch, batch_size, g_pretrained_path, d_pretrained_path, logger, overtraining_detector=False, overtraining_threshold=50):

    pretrained = True
    if g_pretrained_path == "" or d_pretrained_path == "":
        logger.info("g_pretrained_path or d_pretrained_path is null")
        logger.info("Training from scratch!")
        pretrained = False
    
    rvc_version = "v2"
    sample_rate = 48000
    save_only_latest = False
    save_every_weights = True
    gpu = 0
    pitch_guidance = True
    custom_pretrained = True
    cache_data_in_gpu = False
    index_algorithm = "Auto"

    logger.info("===TRAIN===")
    logger.info(f"model_name {model_name}")
    logger.info(f"rvc_version {rvc_version}")
    logger.info(f"sample_rate {sample_rate}")
    logger.info(f"save_every_epoch {save_every_epoch}")
    logger.info(f"save_only_latest {save_only_latest}")
    logger.info(f"save_every_weights {save_every_weights}")
    logger.info(f"total_epoch {total_epoch}")
    logger.info(f"batch_size {batch_size}")
    logger.info(f"gpu {gpu}")
    logger.info(f"pitch_guidance {pitch_guidance}")
    logger.info(f"pretrained {pretrained}")
    logger.info(f"custom_pretrained {custom_pretrained}")
    logger.info(f"g_pretrained_path {g_pretrained_path}")
    logger.info(f"d_pretrained_path {d_pretrained_path}")
    logger.info(f"overtraining_detector {overtraining_detector}")
    logger.info(f"overtraining_threshold {overtraining_threshold}")
    logger.info(f"cache_data_in_gpu {cache_data_in_gpu}")
    logger.info(f"index_algorithm {index_algorithm}")
    logger.info("===========")

    cmd = (
        f"venv/bin/python3 rvc_cli.py train "
        f"--model_name {model_name} "
        f"--rvc_version {rvc_version} "
        f"--sample_rate {sample_rate} "
        f"--save_every_epoch {save_every_epoch} "
        f"--save_only_latest {save_only_latest} "
        f"--save_every_weights {save_every_weights} "
        f"--total_epoch {total_epoch} "
        f"--batch_size {batch_size} "
        f"--gpu {gpu} "
        f"--pitch_guidance {pitch_guidance} "
        f"--pretrained {pretrained} "
        f"--custom_pretrained {custom_pretrained} "
        f"--g_pretrained_path {g_pretrained_path} "
        f"--d_pretrained_path {d_pretrained_path} "
        f"--overtraining_detector {overtraining_detector} "
        f"--overtraining_threshold {overtraining_threshold} "
        f"--cache_data_in_gpu {cache_data_in_gpu} "
        f"--index_algorithm {index_algorithm} "
    )
    return run_command(cmd, logger)

# Run all steps
def run_pipeline(
    model_name: str, 
    cpu_cores: int, 
    save_every_epoch: int, 
    total_epoch: int, 
    batch_size: int, 
    pretrained_path: str, 
    cut_preprocess: bool=True, 
    process_effects: bool=True,
    noise_reduction: bool=False, 
    noise_reduction_strength: float=0.7, 
    overtraining_detector: bool=False, 
    overtraining_threshold: int=50, 
    hop_size: int=160,
    skip_preprocessing=False,
    skip_extraction=False,
    skip_training=False):

    # create experiment directory
    Path(f"/workspace/rvc-cli/logs/{model_name}").mkdir(parents=True, exist_ok=True)

    logger = get_logger(f"/workspace/rvc-cli/logs/{model_name}/training.log")

    logger.info("Starting RVC pipeline...")
    
    dataset_dir = os.path.join("datasets", model_name)
    if not os.path.isdir(dataset_dir):
        raise Exception(dataset_dir, " does not exists.")

    # If a single path is provided and it's a directory, look for G.pth and D.pth
    if pretrained_path != "" and not os.path.isdir(pretrained_path):
        raise Exception("Directory with pretrained does not exists.")
    
    if pretrained_path != "":
        g_pretrained_path = os.path.join(pretrained_path, 'G.pth')
        d_pretrained_path = os.path.join(pretrained_path, 'D.pth')
    else:
        g_pretrained_path = ""
        d_pretrained_path = ""


    if not os.path.isfile(g_pretrained_path):
        raise Exception("G.pth file does not exists: ", g_pretrained_path)
    
    if not os.path.isfile(d_pretrained_path):
        raise Exception("D.pth file does not exists: ", d_pretrained_path)

    if not os.path.exists("venv"):
        raise Exception("It seems that you didn't install app. Run these scripts please:\nchmod +x install.sh\n./install.sh")
    
    if skip_preprocessing == False:
        logger.info("1. Running preprocessing...")
        print("1. Running preprocessing...")
        run_preprocess(model_name, cpu_cores, cut_preprocess, process_effects, noise_reduction, noise_reduction_strength, logger)
    else:
        logger.info("1. Skipping preprocessing...")
        print("1. Skipping preprocessing...")
    
    if skip_extraction == False:
        logger.info("2. Running feature extraction...")
        print("2. Running feature extraction...")
        run_extract(model_name, cpu_cores, hop_size, logger)
    else:
        logger.info("2. Skipping feature extraction...")
        print("2. Skipping feature extraction...")

    if skip_training == False:
        logger.info("3. Running training...")
        print("3. Running training...")

        run_train(model_name, save_every_epoch, total_epoch, batch_size, g_pretrained_path, d_pretrained_path, logger, overtraining_detector, overtraining_threshold)
    else:
        logger.info("3. Skipping training...")
        print("3. Skipping training...")

    logger.info("Pipeline completed successfully!")
    print("Pipeline completed successfully!")