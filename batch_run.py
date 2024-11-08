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
def run_preprocess(model_name):
    cmd = (
        f"venv/bin/python3 rvc_cli.py preprocess "
        f"--model_name {model_name} "
        f"--dataset_path dataset "
        f"--sample_rate 48000 "
        f"--cut_preprocess True "
    )
    return run_command(cmd)

# Extract command
def run_extract(model_name, cpu_cores):
    cmd = (
        f"venv/bin/python3 rvc_cli.py extract "
        f"--model_name {model_name} "
        f"--sample_rate 48000 "
        f"--gpu 0 "
        f"--cpu_cores {cpu_cores} "
    )
    return run_command(cmd)

# Train command
def run_train(model_name, total_epoch):
    cmd = (
        f"venv/bin/python3 rvc_cli.py train "
        f"--model_name {model_name} "
        f"--sample_rate 48000 "
        f"--save_every_epoch 10 "
        f"--total_epoch {total_epoch}"
    )
    return run_command(cmd)

# Run all steps
def run_pipeline(model_name, cpu_cores, total_epoch):
    print("Starting RVC pipeline...")

    if os.path.exists("venv"):
        raise Exception("It seems that you didn't install app. Run these scripts please:\nchmod +x install.sh\n./install.sh")
    
    print("\n1. Running preprocessing...")
    if not run_preprocess(model_name):
        return
    
    print("\n2. Running feature extraction...")
    if not run_extract(model_name, cpu_cores):
        return
    
    print("\n3. Running training...")
    if not run_train(model_name, total_epoch):
        return
    
    print("\nPipeline completed successfully!")