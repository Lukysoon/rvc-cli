import os
import tempfile

from scipy.io import wavfile

from configs.config import Config
from infer.modules.vc.modules import VC
from tools.voicerary_audioprocessing.error_messages import ERR_INFERENCE, ERR_INFERENCE_INVALID_CONVERTED_FILE, \
    INTERNAL_ERR_MESSAGES, USER_FRIENDLY_ERR_MESSAGES
from tools.voicerary_audioprocessing.model import Model
from tools.voicerary_audioprocessing.voicerary_exception import VoiceraryException


class Inference:

    def __init__(self,
                 f0method: str,
                 f0up_key: int,
                 filter_radius: int,
                 index_rate: float,
                 input_audio_path: str,
                 model: Model,
                 protect: float,
                 resample_sr: int,
                 rms_mix_rate: float,
                 auto_pitch_correction_semitones: int = 0):
        self._auto_pitch_correction_semitones = auto_pitch_correction_semitones
        self._f0method = f0method
        self._f0up_key = f0up_key
        self._filter_radius = filter_radius
        self._index_path = model.index_path if model.index_path else model.find_model_index()
        self._index_rate = index_rate
        self._input_audio_path = input_audio_path
        self._protect = protect
        self._resample_sr = resample_sr
        self._rms_mix_rate = rms_mix_rate
        config = Config()
        vc = VC(config)
        vc.get_vc(os.path.basename(model.model_path if model.model_path else model.find_model_path()))
        self._vc = vc

    def do_inference(self, expected_output_path: str = '') -> str:
        _, wav_output = self._vc.vc_single(
            0,
            self._input_audio_path,
            self._f0up_key + self._auto_pitch_correction_semitones,
            None,
            self._f0method,
            self._index_path,
            '',
            self._index_rate,
            self._filter_radius,
            self._resample_sr,
            self._rms_mix_rate,
            self._protect,
        )
        if not _.startswith('Success'):
            raise VoiceraryException(INTERNAL_ERR_MESSAGES[ERR_INFERENCE].format(inference_traceback=_),
                                     USER_FRIENDLY_ERR_MESSAGES[ERR_INFERENCE])

        out = expected_output_path if expected_output_path else tempfile.mkstemp('.wav')[1]
        wavfile.write(out, wav_output[0], wav_output[1])

        if not os.path.isfile(out) or not os.stat(out).st_size > 0:
            raise VoiceraryException(INTERNAL_ERR_MESSAGES[ERR_INFERENCE_INVALID_CONVERTED_FILE].format(out=out),
                                     USER_FRIENDLY_ERR_MESSAGES[ERR_INFERENCE_INVALID_CONVERTED_FILE])

        return out
