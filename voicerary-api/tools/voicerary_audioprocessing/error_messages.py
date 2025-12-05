# Error messages keys definition
ERR_ENV_VAR_NOT_SET = 'err_env_var_not_set'
ERR_FILE_IS_NOT_READABLE = 'err_file_is_not_readable'
ERR_FILE_NOT_EXISTS = 'err_file_not_exists'
ERR_GENERAL = 'err_general'
ERR_GET_FILE_CLOUD = 'err_get_file_cloud'
ERR_INFERENCE = 'err_inference'
ERR_INFERENCE_INVALID_CONVERTED_FILE = 'err_inference_invalid_converted_file'
ERR_INVALID_AUDIO_FILE = 'err_invalid_audio_file'
ERR_INVALID_CONTEXT = 'err_invalid_context'
ERR_INVALID_FILE_FOR_PROCESSING = 'err_invalid_file_for_processing'
ERR_INVALID_FILE_PITCH = 'err_invalid_file_pitch'
ERR_INVALID_MODEL_AGE = 'err_invalid_model_age'
ERR_INVALID_MODEL_GENDER = 'err_invalid_model_gender'
ERR_INVALID_MODEL_METADATA_FILE = 'err_invalid_model_metadata_file'
ERR_INVALID_PAYLOAD = 'err_invalid_payload'
ERR_INVALID_PROCESSING_MODE = 'err_invalid_processing_mode'
ERR_LONG_DURATION = 'err_long_duration'
ERR_LOW_LOUDNESS_LEVEL = 'err_low_loudness_level'
ERR_MODEL_METADATA_API_FETCH = 'err_model_metadata_api_fetch'
ERR_MODEL_NOT_FOUND = 'err_model_not_found'
ERR_NO_AUDIO_STREAM = 'err_no_audio_stream'
ERR_NO_LUFS_VALUE = 'err_no_lufs_value'
ERR_NO_RMS_VALUE = 'err_no_rms_value'
ERR_PAYLOAD_KEY_NOT_EXISTS = 'err_payload_key_not_exists'
ERR_PROCESSING_FAILED = 'err_processing_failed'
ERR_PUT_FILE_CLOUD = 'err_put_file_cloud'
ERR_SHORT_DURATION = 'err_short_duration'

# Error messages with details to store in logs, not to show in response
INTERNAL_ERR_MESSAGES = {
    ERR_ENV_VAR_NOT_SET: "Environment variable {var} is not set",
    ERR_FILE_IS_NOT_READABLE: "File is not readable: {file_path}",
    ERR_FILE_NOT_EXISTS: "File '{file_path}' does not exist",
    ERR_GENERAL: "General error: {err}",
    ERR_GET_FILE_CLOUD: "Download error for {src_path}: local file {local_path} not exists",
    ERR_INFERENCE: "Inference error: {inference_traceback}",
    ERR_INFERENCE_INVALID_CONVERTED_FILE: "Inference error: output file {out} does not exists or empty",
    ERR_INVALID_AUDIO_FILE: "Invalid audio file {file_path}\n{ffmpeg_err}",
    ERR_INVALID_CONTEXT: "Invalid context {context}",
    ERR_INVALID_FILE_FOR_PROCESSING: "File is invalid for further processing",
    ERR_INVALID_FILE_PITCH: "File has highest pitch {file_f0max} while selected model is capable only up to {model_f0max}",
    ERR_INVALID_MODEL_AGE: "Wrong age value for a model instance: {age}",
    ERR_INVALID_MODEL_GENDER: "Wrong gender value for a model instance: {gender}",
    ERR_INVALID_MODEL_METADATA_FILE: "Invalid json content in models metadata file: {file_path}",
    ERR_INVALID_PAYLOAD: "Invalid payload: {err}",
    ERR_INVALID_PROCESSING_MODE: "Invalid processing mode {mode}",
    ERR_LONG_DURATION: "Audio file too long: {duration}s",
    ERR_LOW_LOUDNESS_LEVEL: "Audio file too quiet, RMS is {rms}dB and LUFS is {lufs}dB",
    ERR_MODEL_METADATA_API_FETCH: "Model metadata api request to {url} failed with code {code} and message {message}",
    ERR_MODEL_NOT_FOUND: "Model not found: {model}",
    ERR_NO_AUDIO_STREAM: "File does not contain audio stream",
    ERR_NO_LUFS_VALUE: "Failed to calculate LUFS level for file {file_path}\n{stdout_err}",
    ERR_NO_RMS_VALUE: "Failed to calculate RMS level for file {file_path}\n{stdout_err}",
    ERR_PAYLOAD_KEY_NOT_EXISTS: "Key {key} does not exist in payload",
    ERR_PROCESSING_FAILED: "Whole job has failed",
    ERR_PUT_FILE_CLOUD: "Upload error for {dst_path}: local file {src_path} not exists",
    ERR_SHORT_DURATION: "Audio file too short: {duration}s",
}

# Messages to be returned in error response
USER_FRIENDLY_ERR_MESSAGES = {
    ERR_ENV_VAR_NOT_SET: "Internal error. Ask for support",
    ERR_FILE_IS_NOT_READABLE: "Internal error. Ask for support",
    ERR_FILE_NOT_EXISTS: "We cannot find your file. Try again",
    ERR_GENERAL: "General error. Ask for support",
    ERR_GET_FILE_CLOUD: "Cannot download your file from the cloud storage. Try again",
    ERR_INFERENCE: "Something went wrong during inference process. Try again",
    ERR_INFERENCE_INVALID_CONVERTED_FILE: "Something went wrong during inference process. Try again",
    ERR_INVALID_AUDIO_FILE: "Your file is not suitable for conversion. Ask for support",
    ERR_INVALID_CONTEXT: "Internal error. Ask for support",
    ERR_INVALID_FILE_FOR_PROCESSING: "Your file is not suitable for conversion. Ask for support",
    ERR_INVALID_FILE_PITCH: "Sorry, but this voice cannot hit such high notes. Select other voice",
    ERR_INVALID_MODEL_AGE: "Internal error. Ask for support",
    ERR_INVALID_MODEL_GENDER: "Internal error. Ask for support",
    ERR_INVALID_MODEL_METADATA_FILE: "Internal error. Ask for support",
    ERR_INVALID_PAYLOAD: "Something wrong with your request. Ask for support",
    ERR_INVALID_PROCESSING_MODE: "Internal error. Ask for support",
    ERR_LONG_DURATION: "Your audio is too long, max allowed duration is {max_duration} min",
    ERR_LOW_LOUDNESS_LEVEL: "Your audio is too quiet, try to increase loudness level above {min_rms}dB",
    ERR_MODEL_METADATA_API_FETCH: "Internal error. Ask for support",
    ERR_MODEL_NOT_FOUND: "We cannot find a voice you selected for processing. Ask for support",
    ERR_NO_AUDIO_STREAM: "Your audio file does not seem to contain actual audio. Check your file",
    ERR_NO_LUFS_VALUE: "Something went wrong during LUFS level detection. Ask for support",
    ERR_NO_RMS_VALUE: "Something went wrong during RMS level detection. Ask for support",
    ERR_PAYLOAD_KEY_NOT_EXISTS: "Something wrong with your request. Ask for support",
    ERR_PROCESSING_FAILED: "Your request has failed. Ask for support",
    ERR_PUT_FILE_CLOUD: "Cannot upload your file to the cloud storage. Try again",
    ERR_SHORT_DURATION: "Your audio is too short, it should have a duration at least {min_duration}s",
}

CONTACT_SUPPORT = "({id})."
