import subprocess
import os

def run_command(command):

    try:
        print(f"Executing: {command}")
        
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
def run_preprocess(model_name, dataset, cpu_cores, cut_preprocess, noise_reduction, noise_reduction_strength):
    cmd = (
        f"venv/bin/python3 rvc_cli.py preprocess "
        f"--model_name {model_name} "
        f"--dataset_path {dataset} "
        f"--sample_rate 48000 "
        f"--cpu_cores {cpu_cores} "
        f"--cut_preprocess {cpu_cores} "
        f"--process_effects {cut_preprocess} "
        f"--noise_reduction {noise_reduction} "
        f"--noise_reduction_strength {noise_reduction_strength} "
    )
    return run_command(cmd)

# Extract command
def run_extract(model_name, cpu_cores, hop_size=128):
    cmd = (
        f"venv/bin/python3 rvc_cli.py extract "
        f"--model_name {model_name} "
        f"--rvc_version v2 "
        f"--f0_method rmvpe_gpu"
        f"--pitch_guidance True"
        f"--hop_length {hop_size}"
        f"--cpu_cores {cpu_cores} "
        f"--gpu 0 "
        f"--sample_rate 48000 "
        f"--embedder_model contentvec "
    )
    return run_command(cmd)

# Train command
def run_train(model_name, save_every_epoch, total_epoch, batch_size, g_pretrained_path, d_pretrained_path, overtraining_detector=False, overtraining_threshold=50):

    pretrained = True
    if g_pretrained_path is "" or d_pretrained_path is "":
        print("g_pretrained_path or d_pretrained_path is null")
        print("Training from scratch!")
        pretrained = False

    cmd = (
        f"venv/bin/python3 rvc_cli.py train "
        f"--model_name {model_name} "
        f"--rvc_version v2 "
        f"--sample_rate 48000 "
        f"--save_every_epoch {save_every_epoch} "
        f"--save_only_latest True "
        f"--save_every_weights True "
        f"--total_epoch {total_epoch} "
        f"--sample_rate 48000 "
        f"--batch_size {batch_size} "
        f"--gpu 0 "
        f"--pitch_guidance True "
        f"--pretrained True {pretrained}"
        f"--custom_pretrained True "
        f"--g_pretrained_path {g_pretrained_path} "
        f"--d_pretrained_path {d_pretrained_path} "
        f"--overtraining_detector {overtraining_detector} "
        f"--overtraining_threshold {overtraining_threshold} "
        f"--cache_data_in_gpu False "
        f"--index_algorithm Auto "
    )
    return run_command(cmd)

# Run all steps
def run_pipeline(
        model_name, 
        dataset, 
        cpu_cores, 
        save_every_epoch, 
        total_epoch, 
        batch_size, 
        g_pretrained_path, 
        d_pretrained_path, 
        cut_preprocess=True, 
        noise_reduction=False, 
        noise_reduction_strength=0.7, 
        overtraining_detector=False, 
        overtraining_threshold=50, 
        hop_size=160):
    print("Starting RVC pipeline...")

    if not os.path.exists("venv"):
        raise Exception("It seems that you didn't install app. Run these scripts please:\nchmod +x install.sh\n./install.sh")
    
    print("\n1. Running preprocessing...")
    if not run_preprocess(model_name, dataset, cpu_cores, cut_preprocess, noise_reduction, noise_reduction_strength):
        return
    
    print("\n2. Running feature extraction...")
    if not run_extract(model_name, cpu_cores, hop_size):
        return
    
    print("\n3. Running training...")
    if not run_train(model_name, save_every_epoch, total_epoch, batch_size, g_pretrained_path, d_pretrained_path, overtraining_detector, overtraining_threshold):
        return
    
    print("\nPipeline completed successfully!")