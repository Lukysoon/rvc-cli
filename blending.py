import subprocess
import os
import logging
from custom_logging import get_logger

def run_command(command, logger):
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
        logger.info(f"Error executing command: {e}")
        logger.info(f"Error output: {e.stderr}")
        raise Exception(e.stderr)

def run_blending(model_name, pth_path_1, pth_path_2, ratio, logger):
    logger.info("===BLEND===")
    logger.info(f"model_name {model_name}")
    logger.info(f"pth_path_1 {pth_path_1}")
    logger.info(f"pth_path_2 {pth_path_2}")
    logger.info(f"ratio {ratio}")
    logger.info("===========")

    cmd = (
        f"venv/bin/python3 rvc_cli.py model_blender "
        f"--model_name {model_name} "       
        f"--pth_path_1 {pth_path_1} "
        f"--pth_path_2 {pth_path_2} "
        f"--ratio {ratio} "
        )
    return run_command(cmd, logger)

def run_pipeline(model_name: str, pth_path_1: str, pth_path_2: str, ratio: float):
    logger = get_logger(f"/workspace/rvc-cli/blending.log")
    logger.info("Starting RVC Blending...")
    
    if pth_path_1 == "pth_path_1.pth":
        raise Exception("Change 'pth_path_1.pth' to something else.")

    if pth_path_2 == "pth_path_2.pth":
        raise Exception("Change 'pth_path_2.pth' to something else.")

    if not os.path.exists("venv"):
        raise Exception("It seems that you didn't install the app. Run these scripts please:\nchmod +x install.sh\n./install.sh")

    logger.info("Running blending...")
    print("Running blending...")
    if not run_blending(model_name, pth_path_1, pth_path_2, ratio, logger):
        return
    
    logger.info(f"Blended file was saved to '{os.path.join('logs', model_name + '.pth')}'")
    logger.info("\Blending completed successfully!")

    print(f"Blended file was saved to '{os.path.join('logs', model_name + '.pth')}'")
    print("\Blending completed successfully!")