import subprocess
import os
import logging
from rvc_cli import run_train_script, run_extract_script, run_preprocess_script

# Preprocess command
def run_preprocess(model_name, cpu_cores, cut_preprocess, process_effects, noise_reduction, noise_reduction_strength):
    
    try:
        sample_rate = 48000
        dataset_path = os.path.join("datasets", model_name)

        preproces_log = f'''
        ===PREPROCESS==
        model_name {model_name}
        dataset_path {dataset_path}
        sample_rate {sample_rate}
        cpu_cores {cpu_cores}
        cut_preprocess {cut_preprocess}
        process_effects {process_effects}
        noise_reduction {noise_reduction}
        noise_reduction_strength {noise_reduction_strength}
        ===============\n'''
        print(preproces_log)
        logging.INFO(preproces_log)

        run_preprocess_script(
            model_name,
            dataset_path,
            sample_rate,
            cpu_cores,
            cut_preprocess,
            process_effects,
            noise_reduction,
            noise_reduction_strength)

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

        extract_log = f'''
        ===EXTRACT FEATURES===
        model_name {model_name}
        rvc_version {rvc_version}
        f0_method {f0_method}
        pitch_guidance {pitch_guidance}
        hop_length {hop_size}
        cpu_cores {cpu_cores}
        gpu {gpu}
        sample_rate {sample_rate}
        embedder_model {embedder_model}
        ====================\n'''

        print(extract_log)
        logging.INFO(extract_log)

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
            print(f"Using pretrained D model '{d_pretrained_path}'")
            print(f"Using pretrained G model '{g_pretrained_path}'")
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

        train_log = f'''
        ===TRAIN===
        model_name {model_name}")
        rvc_version {rvc_version}")
        save_every_epoch {save_every_epoch}")
        save_only_latest {save_only_latest}")
        save_every_weights {save_every_weights}")
        total_epoch {total_epoch}")
        sample_rate {sample_rate}")
        batch_size {batch_size}")
        gpu {gpu}")
        pitch_guidance {pitch_guidance}")
        overtraining_detector {overtraining_detector}")
        overtraining_threshold {overtraining_threshold}")
        pretrained {pretrained}")
        cleanup {cleanup}")
        index_algorithm {index_algorithm}")
        cache_data_in_gpu {cache_data_in_gpu}")
        custom_pretrained {custom_pretrained}")
        g_pretrained_path {g_pretrained_path}")
        d_pretrained_path {d_pretrained_path}")
        ==========='''

        print(train_log)
        logging.INFO(train_log)

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
            raise Exception(f"Directory '{pretrained_dir}' doesn't exist.")

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
    logging.basicConfig(filename=os.path.join(experiment_path, "train_logs.txt"),
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)