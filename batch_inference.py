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

def run_batch_infer(
    pitch, filter_radius, index_rate, volume_envelope, protect, hop_length, f0_method,
    input_dir_path, output_dir_path, pth_path, index_path, split_audio, f0_autotune, clean_audio, clean_strength,
    export_format, embedder_model, embedder_model_custom, upscale_audio, f0_file, formant_shifting,
    formant_qfrency, formant_timbre, sid, post_process, reverb, pitch_shift, limiter, gain, distortion,
    chorus, bitcrush, clipping, compressor, delay, reverb_room_size, reverb_damping, reverb_wet_gain,
    reverb_dry_gain, reverb_width, reverb_freeze_mode, pitch_shift_semitones, limiter_threshold,
    limiter_release_time, gain_db, distortion_gain, chorus_rate, chorus_depth, chorus_center_delay,
    chorus_feedback, chorus_mix, bitcrush_bit_depth, clipping_threshold, compressor_threshold,
    compressor_ratio, compressor_attack, compressor_release, delay_seconds, delay_feedback, delay_mix
):
    print("===BATCH INFER===")
    print(f"pitch {pitch}")
    print(f"filter_radius {filter_radius}")
    print(f"index_rate {index_rate}")
    print(f"volume_envelope {volume_envelope}")
    print(f"protect {protect}")
    print(f"hop_length {hop_length}")
    print(f"f0_method {f0_method}")
    print(f"input_dir_path {input_dir_path}")
    print(f"output_dir_path {output_dir_path}")
    print(f"pth_path {pth_path}")
    print(f"index_path {index_path}")
    print(f"split_audio {split_audio}")
    print(f"f0_autotune {f0_autotune}")
    print(f"clean_audio {clean_audio}")
    print(f"clean_strength {clean_strength}")
    print(f"export_format {export_format}")
    print(f"embedder_model {embedder_model}")
    print(f"embedder_model_custom {embedder_model_custom}")
    print(f"upscale_audio {upscale_audio}")
    print(f"f0_file {f0_file}")
    print(f"formant_shifting {formant_shifting}")
    print(f"formant_qfrency {formant_qfrency}")
    print(f"formant_timbre {formant_timbre}")
    print(f"sid {sid}")
    print(f"post_process {post_process}")
    print(f"reverb {reverb}")
    print(f"pitch_shift {pitch_shift}")
    print(f"limiter {limiter}")
    print(f"gain {gain}")
    print(f"distortion {distortion}")
    print(f"chorus {chorus}")
    print(f"bitcrush {bitcrush}")
    print(f"clipping {clipping}")
    print(f"compressor {compressor}")
    print(f"delay {delay}")
    print(f"reverb_room_size {reverb_room_size}")
    print(f"reverb_damping {reverb_damping}")
    print(f"reverb_wet_gain {reverb_wet_gain}")
    print(f"reverb_dry_gain {reverb_dry_gain}")
    print(f"reverb_width {reverb_width}")
    print(f"reverb_freeze_mode {reverb_freeze_mode}")
    print(f"pitch_shift_semitones {pitch_shift_semitones}")
    print(f"limiter_threshold {limiter_threshold}")
    print(f"limiter_release_time {limiter_release_time}")
    print(f"gain_db {gain_db}")
    print(f"distortion_gain {distortion_gain}")
    print(f"chorus_rate {chorus_rate}")
    print(f"chorus_depth {chorus_depth}")
    print(f"chorus_center_delay {chorus_center_delay}")
    print(f"chorus_feedback {chorus_feedback}")
    print(f"chorus_mix {chorus_mix}")
    print(f"bitcrush_bit_depth {bitcrush_bit_depth}")
    print(f"clipping_threshold {clipping_threshold}")
    print(f"compressor_threshold {compressor_threshold}")
    print(f"compressor_ratio {compressor_ratio}")
    print(f"compressor_attack {compressor_attack}")
    print(f"compressor_release {compressor_release}")
    print(f"delay_seconds {delay_seconds}")
    print(f"delay_feedback {delay_feedback}")
    print(f"delay_mix {delay_mix}")
    print("===========\n")

    cmd = (
        f"venv/bin/python3 rvc_cli.py batch_infer "
        f"--pitch {pitch} "
        f"--filter_radius {filter_radius} "
        f"--index_rate {index_rate} "
        f"--volume_envelope {volume_envelope} "
        f"--protect {protect} "
        f"--hop_length {hop_length} "
        f"--f0_method {f0_method} "
        f"--input_folder {input_dir_path} "
        f"--output_folder {output_dir_path} "
        f"--pth_path {pth_path} "
        f"--index_path {index_path} "
        f"--split_audio {split_audio} "
        f"--f0_autotune {f0_autotune} "
        f"--clean_audio {clean_audio} "
        f"--clean_strength {clean_strength} "
        f"--export_format {export_format} "
        f"--embedder_model {embedder_model} "
        f"--embedder_model_custom {embedder_model_custom} "
        f"--upscale_audio {upscale_audio} "
        f"--f0_file {f0_file} "
        f"--formant_shifting {formant_shifting} "
        f"--formant_qfrency {formant_qfrency} "
        f"--formant_timbre {formant_timbre} "
        f"--sid {sid} "
        f"--post_process {post_process} "
        f"--reverb {reverb} "
        f"--pitch_shift {pitch_shift} "
        f"--limiter {limiter} "
        f"--gain {gain} "
        f"--distortion {distortion} "
        f"--chorus {chorus} "
        f"--bitcrush {bitcrush} "
        f"--clipping {clipping} "
        f"--compressor {compressor} "
        f"--delay {delay} "
        f"--reverb_room_size {reverb_room_size} "
        f"--reverb_damping {reverb_damping} "
        f"--reverb_wet_gain {reverb_wet_gain} "
        f"--reverb_dry_gain {reverb_dry_gain} "
        f"--reverb_width {reverb_width} "
        f"--reverb_freeze_mode {reverb_freeze_mode} "
        f"--pitch_shift_semitones {pitch_shift_semitones} "
        f"--limiter_threshold {limiter_threshold} "
        f"--limiter_release_time {limiter_release_time} "
        f"--gain_db {gain_db} "
        f"--distortion_gain {distortion_gain} "
        f"--chorus_rate {chorus_rate} "
        f"--chorus_depth {chorus_depth} "
        f"--chorus_center_delay {chorus_center_delay} "
        f"--chorus_feedback {chorus_feedback} "
        f"--chorus_mix {chorus_mix} "
        f"--bitcrush_bit_depth {bitcrush_bit_depth} "
        f"--clipping_threshold {clipping_threshold} "
        f"--compressor_threshold {compressor_threshold} "
        f"--compressor_ratio {compressor_ratio} "
        f"--compressor_attack {compressor_attack} "
        f"--compressor_release {compressor_release} "
        f"--delay_seconds {delay_seconds} "
        f"--delay_feedback {delay_feedback} "
        f"--delay_mix {delay_mix} "
        )
    return run_command(cmd)

def run_pipeline(
    pitch: int, 
    input_dir_path: str, 
    output_dir_path: str, 
    pth_path: str, 
    filter_radius=3, 
    index_rate=0,
    volume_envelope=0.8, 
    protect=0.33, 
    hop_length=128,
    f0_method="rmvpe",
    index_path="file.index", 
    split_audio=False, 
    f0_autotune=False, 
    clean_audio=False, 
    clean_strength=0.7,
    export_format="WAV", 
    embedder_model="contentvec", 
    embedder_model_custom=None,
    upscale_audio=False, 
    f0_file=None,
    formant_shifting=False,
    formant_qfrency=1.0, 
    formant_timbre=1.0, 
    sid=0, 
    post_process=False,
    reverb=False, 
    pitch_shift=False, 
    limiter=False, 
    gain=False, 
    distortion=False,
    chorus=False, 
    bitcrush=False, 
    clipping=False, 
    compressor=False, 
    delay=False, 
    reverb_room_size=0.5, 
    reverb_damping=0.5, 
    reverb_wet_gain=0.5,
    reverb_dry_gain=0.5, 
    reverb_width=0.5, 
    reverb_freeze_mode=0.5, 
    pitch_shift_semitones=0.0, 
    limiter_threshold=-6,
    limiter_release_time=0.01, 
    gain_db=0.0, 
    distortion_gain=25, 
    chorus_rate=1.0, 
    chorus_depth=0.25, 
    chorus_center_delay=7,
    chorus_feedback=0, 
    chorus_mix=0.5, 
    bitcrush_bit_depth=8, 
    clipping_threshold=-6, 
    compressor_threshold=0.0,
    compressor_ratio=1, 
    compressor_attack=1.0, 
    compressor_release=100, 
    delay_seconds=0.5, 
    delay_feedback=0.0, 
    delay_mix=0.5
    ):
    print("Starting RVC batch inference...")

    if pth_path == "path-to-pth-file.pth":
        raise Exception("Change 'path-to-pth-file.pth' to something else.")

    if not os.path.exists("venv"):
        raise Exception("It seems that you didn't install the app. Run these scripts please:\nchmod +x install.sh\n./install.sh")

    print("\nRunning batch inference...")
    if not run_batch_infer(
        pitch, 
        filter_radius, 
        index_rate, 
        volume_envelope, 
        protect, 
        hop_length, 
        f0_method,
        input_dir_path, 
        output_dir_path, 
        pth_path, 
        index_path, 
        split_audio, 
        f0_autotune, 
        clean_audio, 
        clean_strength,
        export_format, 
        embedder_model, 
        embedder_model_custom, 
        upscale_audio, 
        f0_file, 
        formant_shifting,
        formant_qfrency, 
        formant_timbre, 
        sid, 
        post_process, 
        reverb, 
        pitch_shift, 
        limiter, 
        gain, 
        distortion,
        chorus, 
        bitcrush, 
        clipping, 
        compressor, 
        delay, 
        reverb_room_size, 
        reverb_damping, 
        reverb_wet_gain,
        reverb_dry_gain, 
        reverb_width, 
        reverb_freeze_mode, 
        pitch_shift_semitones, 
        limiter_threshold,
        limiter_release_time, 
        gain_db, 
        distortion_gain, 
        chorus_rate, 
        chorus_depth, 
        chorus_center_delay,
        chorus_feedback, 
        chorus_mix, 
        bitcrush_bit_depth, 
        clipping_threshold, 
        compressor_threshold,
        compressor_ratio, 
        compressor_attack, 
        compressor_release, 
        delay_seconds, 
        delay_feedback, 
        delay_mix
    ):
        return
    
    print("\nBatch inference completed successfully!")