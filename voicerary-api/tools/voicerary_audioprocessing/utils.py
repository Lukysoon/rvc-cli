import glob
import json
import math
import os
import statistics as stats
import tempfile
import time
import uuid

import librosa
import numpy as np
import soundfile as sf
import torch
from dotenv import load_dotenv

from tools.voicerary_audioprocessing.error_messages import CONTACT_SUPPORT
from tools.voicerary_audioprocessing.storage.storage import Storage
from tools.voicerary_audioprocessing.storage.cloud_storage import CloudStorage

load_dotenv()

from infer.lib.rmvpe import RMVPE


class AudioProcessingUtils:
    PROCESSING_SUCCESS = 'success'
    PROCESSING_ERROR = 'error'

    _rmvpe = None

    @staticmethod
    def get_temp_file_path(name: str) -> str:
        return os.path.join(tempfile.gettempdir(), name)

    @staticmethod
    def append_to_temp_file(temp_file_list: str, line: str) -> None:
        with open(temp_file_list, 'a') as f:
            f.write(line)

    @staticmethod
    def remove_temp_files(pattern: str) -> None:
        for temp_file in glob.glob(os.path.join(tempfile.gettempdir(), pattern)):
            os.remove(temp_file)

    @staticmethod
    def semitone_distance(pitch1: float, pitch2: float) -> int:
        if pitch1 == 0.0 or pitch2 == 0.0:
            return 0

        return round(12 * math.log2(pitch1 / pitch2))

    @staticmethod
    def get_fundamental_frequency(wav_audio_file_path: str) -> float:
        f0 = AudioProcessingUtils._do_rmvpe_detection(wav_audio_file_path)
        if len(f0):
            f0_nonzero = f0[f0 != 0]
            if len(f0_nonzero) == 0:
                return 0
            mode_nonzero = stats.multimode(np.round(f0_nonzero))
            return np.average(mode_nonzero)
        else:
            return 0

    @staticmethod
    def get_highest_frequency(wav_audio_file_path: str) -> float:
        f0 = AudioProcessingUtils._do_rmvpe_detection(wav_audio_file_path)
        if len(f0):
            f0_nonzero = f0[f0 != 0]
            if len(f0_nonzero) == 0:
                return 0
            return np.round(np.max(f0_nonzero))
        else:
            return 0

    @staticmethod
    def _do_rmvpe_detection(wav_audio_file_path: str):
        if os.path.isfile(wav_audio_file_path):
            audio, sampling_rate = sf.read(wav_audio_file_path)
            if len(audio.shape) > 1:
                audio = librosa.to_mono(audio.transpose(1, 0))
            if sampling_rate != 16000:
                audio = librosa.resample(audio, orig_sr=sampling_rate, target_sr=16000)
            thred = 0.03  # 0.01
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                device = "cuda"
            else:
                device = "cpu"
            AudioProcessingUtils._rmvpe = RMVPE(os.path.join(os.environ["RMVPE_ROOT"],
                                                             'rmvpe.pt'), is_half=False, device=device)
            result = AudioProcessingUtils._rmvpe.infer_from_audio(audio, thred=thred)
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            del AudioProcessingUtils._rmvpe
            return result
        else:
            return []

    @staticmethod
    def handle_response(payload: dict,
                        storage: Storage = None,
                        processing_result: list = None,
                        ) -> dict:
        task_id = payload["id"] if "id" in payload else f'_{uuid.uuid1()}_'
        response = {
            "processing_result": processing_result,
            "auto_pitch_correction_bypassed": payload["input"]["bypass_auto_pitch"],
            "orig_request_payload": payload
        }
        if storage:
            storage.save_log(Storage.LOG_RESPONSE, task_id, response)
            storage.cleanup()
        else:
            print(json.dumps(response, indent=4))

        # remove not needed data from response
        for item in processing_result:
            item.pop("traceback", None)
            item.pop("error_details", None)
            if item["status"] == AudioProcessingUtils.PROCESSING_ERROR:
                item["error_message"] = f'{item["error_message"]} {CONTACT_SUPPORT.format(id=task_id)}'
        response["processing_result"] = processing_result
        return response

    @staticmethod
    def handle_exception(payload: dict,
                         err_message: str,
                         err_message_for_user: str,
                         traceback: list = None,
                         storage: Storage = None) -> dict:
        task_id = payload["id"] if "id" in payload else f'_{uuid.uuid1()}_'
        err_response = {
            "error": err_message,
            "traceback": traceback if traceback else "",
            "orig_request_payload": payload
        }
        if storage:
            storage.save_log(Storage.LOG_ERROR, task_id, err_response)
            storage.cleanup()
        else:
            # for now, it makes sense to have emergency log storage only for API context and CloudStorage
            emergency_log_storage = CloudStorage.emergency_log_storage()
            if emergency_log_storage:
                emergency_log_storage.save_log(Storage.LOG_ERROR, task_id, err_response)
                emergency_log_storage.cleanup()
            else:
                print(json.dumps(err_response, indent=4))
        error = f'{err_message_for_user} {CONTACT_SUPPORT.format(id=task_id)}'
        return {"error": error}

    @staticmethod
    def get_unique_target_file_remote_path(source_filepath: str, model_name: str, pitch: int, bypass_auto_pitch: bool) -> str:
        source_filepath_no_ext = os.path.splitext(source_filepath)[0]
        singing_flag = '_S' if bypass_auto_pitch else ''
        return f'{source_filepath_no_ext}{singing_flag}_{model_name}_{pitch}_{round(time.time())}.wav'
