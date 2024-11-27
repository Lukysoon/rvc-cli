import subprocess
import os

def run_command(command):

    try:
        # Use shell=True and create a new shell session
        process = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        
        print(process.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Error output: {e.stderr}")
        return False


# Preprocess command
def run_preprocess(model_name, cpu_cores, cut_preprocess, process_effects, noise_reduction, noise_reduction_strength):
    
    sample_rate = 48000
    dataset_path = os.path.join("datasets", model_name)

    print("===PREPROCESS==")
    print(f"model_name {model_name}")
    print(f"dataset_path {dataset_path}")
    print(f"sample_rate {sample_rate}")
    print(f"cpu_cores {cpu_cores}")
    print(f"cut_preprocess {cut_preprocess}")
    print(f"process_effects {process_effects}") 
    print(f"noise_reduction {noise_reduction}")
    print(f"noise_reduction_strength {noise_reduction_strength}")
    print("===============\n")
    
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
    return run_command(cmd)

# Extract command
def run_extract(model_name, cpu_cores, hop_size=128):

    rvc_version = "v2"
    f0_method = "rmvpe"
    pitch_guidance = True
    gpu = 0
    sample_rate = 48000
    embedder_model = "contentvec"

    print("===EXTRACT FEATURES===")
    print(f"model_name {model_name}")
    print(f"rvc_version {rvc_version}")
    print(f"f0_method {f0_method}")
    print(f"pitch_guidance {pitch_guidance}")
    print(f"hop_length {hop_size}")
    print(f"cpu_cores {cpu_cores}")
    print(f"gpu {gpu}")
    print(f"sample_rate {sample_rate}")
    print(f"embedder_model {embedder_model}")
    print("=====================\n")

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
    return run_command(cmd)

# Train command
def run_train(model_name, save_every_epoch, total_epoch, batch_size, g_pretrained_path, d_pretrained_path, overtraining_detector=False, overtraining_threshold=50):

    pretrained = True
    if g_pretrained_path == "" or d_pretrained_path == "":
        print("g_pretrained_path or d_pretrained_path is null")
        print("Training from scratch!")
        pretrained = False
    
    rvc_version = "v2"
    sample_rate = 48000
    save_only_latest = True
    save_every_weights = True
    gpu = 0
    pitch_guidance = True
    custom_pretrained = True
    cache_data_in_gpu = False
    index_algorithm = "Auto"

    print("===TRAIN===")
    print(f"model_name {model_name}")
    print(f"rvc_version {rvc_version}")
    print(f"sample_rate {sample_rate}")
    print(f"save_every_epoch {save_every_epoch}")
    print(f"save_only_latest {save_only_latest}")
    print(f"save_every_weights {save_every_weights}")
    print(f"total_epoch {total_epoch}")
    print(f"batch_size {batch_size}")
    print(f"gpu {gpu}")
    print(f"pitch_guidance {pitch_guidance}")
    print(f"pretrained {pretrained}")
    print(f"custom_pretrained {custom_pretrained}")
    print(f"g_pretrained_path {g_pretrained_path}")
    print(f"d_pretrained_path {d_pretrained_path}")
    print(f"overtraining_detector {overtraining_detector}")
    print(f"overtraining_threshold {overtraining_threshold}")
    print(f"cache_data_in_gpu {cache_data_in_gpu}")
    print(f"index_algorithm {index_algorithm}")
    print("===========\n")

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
    return run_command(cmd)

# Run all steps
def run_pipeline(
    model_name: str, 
    cpu_cores: int, 
    save_every_epoch: int, 
    total_epoch: int, 
    batch_size: int, 
    g_pretrained_path: str, 
    d_pretrained_path: str, 
    cut_preprocess: bool=True, 
    process_effects: bool=True,
    noise_reduction: bool=False, 
    noise_reduction_strength: float=0.7, 
    overtraining_detector: bool=False, 
    overtraining_threshold: int=50, 
    hop_size: int=160):
    print("Starting RVC pipeline...")

    if not os.path.exists("venv"):
        raise Exception("It seems that you didn't install app. Run these scripts please:\nchmod +x install.sh\n./install.sh")
    
    print("\n1. Running preprocessing...")
    if not run_preprocess(model_name, cpu_cores, cut_preprocess, process_effects, noise_reduction, noise_reduction_strength):
        return
    
    print("\n2. Running feature extraction...")
    if not run_extract(model_name, cpu_cores, hop_size):
        return
    
    print("\n3. Running training...")
    if not run_train(model_name, save_every_epoch, total_epoch, batch_size, g_pretrained_path, d_pretrained_path, overtraining_detector, overtraining_threshold):
        return
    
    print("\nPipeline completed successfully!")