import subprocess
import os
import logging

def run_command(command):
    try:
        process = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )

        logging.info(process.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Error output: {e.stderr}")
        return False

def run_infer(model_name, pth_path_1, pth_path_2, ratio):
    print("===BLEND===")
    print(f"model_name {model_name}")
    print(f"pth_path_1 {pth_path_1}")
    print(f"pth_path_2 {pth_path_2}")
    print(f"ratio {ratio}")
    print("===========\n")

    cmd = (
        f"venv/bin/python3 rvc_cli.py model_blender "
        f"--model_name {model_name} "       
        f"--pth_path_1 {pth_path_1} "
        f"--pth_path_2 {pth_path_2} "
        f"--ratio {ratio} "
        )
    return run_command(cmd)

def run_pipeline(model_name: str, pth_path_1: str, pth_path_2: str, ratio: float):
    print("Starting RVC Blending...")
    
    if pth_path_1 == "pth_path_1.pth":
        raise Exception("Change 'pth_path_1.pth' to something else.")

    if pth_path_2 == "pth_path_2.pth":
        raise Exception("Change 'pth_path_2.pth' to something else.")

    if not os.path.exists("venv"):
        raise Exception("It seems that you didn't install the app. Run these scripts please:\nchmod +x install.sh\n./install.sh")

    print("\nRunning blending...")
    if not run_infer(model_name, pth_path_1, pth_path_2, ratio):
        return
    
    print(f"Blended file was saved to '{os.path.join("logs", model_name + ".pth")}'")
    print("\Blending completed successfully!")