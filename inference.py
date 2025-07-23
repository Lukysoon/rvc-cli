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

        return True
    except subprocess.CalledProcessError as e:
        logger.info(f"Error executing command: {e}")
        logger.info(f"Error output: {e.stderr}")
        raise Exception(e.stderr)

def run_infer(
    pitch, filter_radius, index_rate, volume_envelope, protect, hop_length, f0_method,
    input_path, output_path, pth_path, index_path, split_audio, f0_autotune, clean_audio, clean_strength,
    export_format, embedder_model, embedder_model_custom, upscale_audio, f0_file, formant_shifting,
    formant_qfrency, formant_timbre, sid, post_process, reverb, pitch_shift, limiter, gain, distortion,
    chorus, bitcrush, clipping, compressor, delay, reverb_room_size, reverb_damping, reverb_wet_gain,
    reverb_dry_gain, reverb_width, reverb_freeze_mode, pitch_shift_semitones, limiter_threshold,
    limiter_release_time, gain_db, distortion_gain, chorus_rate, chorus_depth, chorus_center_delay,
    chorus_feedback, chorus_mix, bitcrush_bit_depth, clipping_threshold, compressor_threshold,
    compressor_ratio, compressor_attack, compressor_release, delay_seconds, delay_feedback, delay_mix, logger
):
    logger.info("===INFER===")
    logger.info(f"pitch {pitch}")
    logger.info(f"filter_radius {filter_radius}")
    logger.info(f"index_rate {index_rate}")
    logger.info(f"volume_envelope {volume_envelope}")
    logger.info(f"protect {protect}")
    logger.info(f"hop_length {hop_length}")
    logger.info(f"f0_method {f0_method}")
    logger.info(f"input_path {input_path}")
    logger.info(f"output_path {output_path}")
    logger.info(f"pth_path {pth_path}")
    logger.info(f"index_path {index_path}")
    logger.info(f"split_audio {split_audio}")
    logger.info(f"f0_autotune {f0_autotune}")
    logger.info(f"clean_audio {clean_audio}")
    logger.info(f"clean_strength {clean_strength}")
    logger.info(f"export_format {export_format}")
    logger.info(f"embedder_model {embedder_model}")
    logger.info(f"embedder_model_custom {embedder_model_custom}")
    logger.info(f"upscale_audio {upscale_audio}")
    logger.info(f"f0_file {f0_file}")
    logger.info(f"formant_shifting {formant_shifting}")
    logger.info(f"formant_qfrency {formant_qfrency}")
    logger.info(f"formant_timbre {formant_timbre}")
    logger.info(f"sid {sid}")
    logger.info(f"post_process {post_process}")
    logger.info(f"reverb {reverb}")
    logger.info(f"pitch_shift {pitch_shift}")
    logger.info(f"limiter {limiter}")
    logger.info(f"gain {gain}")
    logger.info(f"distortion {distortion}")
    logger.info(f"chorus {chorus}")
    logger.info(f"bitcrush {bitcrush}")
    logger.info(f"clipping {clipping}")
    logger.info(f"compressor {compressor}")
    logger.info(f"delay {delay}")
    logger.info(f"reverb_room_size {reverb_room_size}")
    logger.info(f"reverb_damping {reverb_damping}")
    logger.info(f"reverb_wet_gain {reverb_wet_gain}")
    logger.info(f"reverb_dry_gain {reverb_dry_gain}")
    logger.info(f"reverb_width {reverb_width}")
    logger.info(f"reverb_freeze_mode {reverb_freeze_mode}")
    logger.info(f"pitch_shift_semitones {pitch_shift_semitones}")
    logger.info(f"limiter_threshold {limiter_threshold}")
    logger.info(f"limiter_release_time {limiter_release_time}")
    logger.info(f"gain_db {gain_db}")
    logger.info(f"distortion_gain {distortion_gain}")
    logger.info(f"chorus_rate {chorus_rate}")
    logger.info(f"chorus_depth {chorus_depth}")
    logger.info(f"chorus_center_delay {chorus_center_delay}")
    logger.info(f"chorus_feedback {chorus_feedback}")
    logger.info(f"chorus_mix {chorus_mix}")
    logger.info(f"bitcrush_bit_depth {bitcrush_bit_depth}")
    logger.info(f"clipping_threshold {clipping_threshold}")
    logger.info(f"compressor_threshold {compressor_threshold}")
    logger.info(f"compressor_ratio {compressor_ratio}")
    logger.info(f"compressor_attack {compressor_attack}")
    logger.info(f"compressor_release {compressor_release}")
    logger.info(f"delay_seconds {delay_seconds}")
    logger.info(f"delay_feedback {delay_feedback}")
    logger.info(f"delay_mix {delay_mix}")
    logger.info("===========")

    cmd = (
        f"venv/bin/python3 rvc_cli.py infer "
        f"--pitch {pitch} "
        f"--filter_radius {filter_radius} "
        f"--index_rate {index_rate} "
        f"--volume_envelope {volume_envelope} "
        f"--protect {protect} "
        f"--hop_length {hop_length} "
        f"--f0_method {f0_method} "
        f"--input_path {input_path} "
        f"--output_path {output_path} "
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
    return run_command(cmd, logger)

def run_pipeline(
    pitch: int, 
    input_path: str, 
    output_path: str, 
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

    log_filename = "inference.log"

    if not os.path.exists(log_filename):
        os.mknod(log_filename)

    logger = get_logger(log_filename)

    logger.info("Starting RVC inference...")

    if not os.path.isfile(input_path):
        raise Exception(f"File {input_path} doesn't exists.")

    if not os.path.isfile(pth_path):
        raise Exception(f"File {pth_path} doesn't exists.")

    if not os.path.exists("venv"):
        raise Exception("It seems that you didn't install the app. Run these scripts please:\nchmod +x install.sh\n./install.sh")

    logger.info("Running inference...")
    print("Running inference...")
    if not run_infer(
        pitch, 
        filter_radius, 
        index_rate, 
        volume_envelope, 
        protect, 
        hop_length, 
        f0_method,
        input_path, 
        output_path, 
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
        delay_mix,
        logger
    ):
        return
    logger.info(f"Output file saved to '{output_path}'")
    logger.info("Inference completed successfully!")

    print(f"Output file saved to '{output_path}'")
    print("Inference completed successfully!")