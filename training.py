import subprocess
import os
import logging
from rvc_cli import run_train_script, run_extract_script, run_preprocess_script

# Preprocess command
def run_preprocess(model_name, cpu_cores, cut_preprocess, process_effects, noise_reduction, noise_reduction_strength):
    
    try:
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
        
        run_preprocess_script(
            model_name,
            dataset_path,
            sample_rate,
            cpu_cores,
            cut_preprocess,
            process_effects,
            noise_reduction,
            noise_reduction_strength
        )

    except Exception as e:
        print("Error in preprocessing:")
        print(e)


# Extract command
def run_extract(model_name, cpu_cores, hop_size):

    try:
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

        run_extract_script(
            model_name,
            rvc_version,
            f0_method,
            pitch_guidance,
            hop_size,
            cpu_cores,
            gpu,
            sample_rate,
            embedder_model
        )
    except Exception as e:
        print("Error in extraction:")
        print(e)


# Train command
def run_train(model_name, save_every_epoch, total_epoch, batch_size, g_pretrained_path, d_pretrained_path, overtraining_detector=False, overtraining_threshold=50):

    try:
        if g_pretrained_path == "" or d_pretrained_path == "":
            print("Pretrained path is null.")
            print("Training from scratch!")
            pretrained = False
        else:
            print(f"Using pretrained D model {d_pretrained_path}")
            print(f"Using pretrained G model {g_pretrained_path}")
            pretrained = True
        
        rvc_version = "v2"
        sample_rate = 48000
        save_only_latest = False
        save_every_weights = True
        gpu = 0
        pitch_guidance = True
        custom_pretrained = True
        cache_data_in_gpu = False
        index_algorithm = "Auto"
        cleanup = False

        print("===TRAIN===")
        print(f"model_name {model_name}")
        print(f"rvc_version {rvc_version}")
        print(f"save_every_epoch {save_every_epoch}")
        print(f"save_only_latest {save_only_latest}")
        print(f"save_every_weights {save_every_weights}")
        print(f"total_epoch {total_epoch}")
        print(f"sample_rate {sample_rate}")
        print(f"batch_size {batch_size}")
        print(f"gpu {gpu}")
        print(f"pitch_guidance {pitch_guidance}")
        print(f"overtraining_detector {overtraining_detector}")
        print(f"overtraining_threshold {overtraining_threshold}")
        print(f"pretrained {pretrained}")
        print(f"cleanup {cleanup}")
        print(f"index_algorithm {index_algorithm}")
        print(f"cache_data_in_gpu {cache_data_in_gpu}")
        print(f"custom_pretrained {custom_pretrained}")
        print(f"g_pretrained_path {g_pretrained_path}")
        print(f"d_pretrained_path {d_pretrained_path}")
        print("===========\n")

        run_train_script(
            model_name, 
            rvc_version, 
            save_every_epoch, 
            save_only_latest, 
            save_every_weights,
            total_epoch, 
            sample_rate, 
            batch_size, 
            gpu, 
            pitch_guidance, 
            overtraining_detector, 
            overtraining_threshold, 
            pretrained, 
            cleanup,
            index_algorithm,
            cache_data_in_gpu, 
            custom_pretrained, 
            g_pretrained_path,
            d_pretrained_path)
        
    except Exception as e:
        print("Error in training:")
        print(e)
    
# Run all steps
def run_pipeline(
    model_name: str, 
    cpu_cores: int, 
    save_every_epoch: int, 
    total_epoch: int, 
    batch_size: int, 
    pretrained_dir: str, 
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

    g_pretrained_path = ""
    d_pretrained_path = ""

    if pretrained_dir != "":
        pretrained_dir = os.path.join("pretrained", pretrained_dir)
        g_pretrained_path = os.path.join(pretrained_dir, "G.pth")
        d_pretrained_path = os.path.join(pretrained_dir, "D.pth")

        if not os.path.isdir(pretrained_dir):
            raise Exception(f"Directory {pretrained_dir} doesn't exist.")

        if (pretrained_dir != "" and not os.path.isfile(g_pretrained_path)):
            raise Exception(f"The file '{g_pretrained_path}' doesn't exist.")

        if (pretrained_dir != "" and not os.path.isfile(d_pretrained_path)):
            raise Exception(f"The file '{d_pretrained_path}' doesn't exist.")

    setup_logs(os.path.join("logs", model_name))
    
    print("\n1. Running preprocessing...")
    run_preprocess(model_name, cpu_cores, cut_preprocess, process_effects, noise_reduction, noise_reduction_strength)
    
    print("\n2. Running feature extraction...")
    run_extract(model_name, cpu_cores, hop_size)
    
    print("\n3. Running training...")
    run_train(model_name, save_every_epoch, total_epoch, batch_size, g_pretrained_path, d_pretrained_path, overtraining_detector, overtraining_threshold)
    
    print("\nPipeline completed successfully!")

def setup_logs(experiment_path):
    if not os.path.exists(experiment_path):
        os.makedirs(experiment_path)

    logger = logging.getLogger("Training")
    logging.basicConfig(filename=os.path.join(experiment_path, "experiment_train_logs.log"),
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)