import os

from tools.voicerary_audioprocessing import Storage, AudioProcessingUtils, AudioProcessing
from tools.voicerary_audioprocessing.inference import Inference
from tools.voicerary_audioprocessing.model import Model
from tools.voicerary_audioprocessing.validator import AudioFileValidator


class VoiceraryPipeline:
    def __init__(self,
                 model: Model,
                 storage: Storage,
                 source_path: str,
                 processing_mode: str,
                 f0method: str,
                 f0up_key: int,
                 filter_radius: int,
                 index_rate: float,
                 protect: float,
                 resample_sr: int,
                 rms_mix_rate: float,
                 bypass_auto_pitch: bool,
                 ):
        self._model = model
        self._storage = storage
        self._processing_mode = processing_mode
        self._f0method = f0method
        self._f0up_key = f0up_key
        self._filter_radius = filter_radius
        self._index_rate = index_rate
        self._protect = protect
        self._resample_sr = resample_sr
        self._rms_mix_rate = rms_mix_rate
        self._bypass_auto_pitch = bypass_auto_pitch

        # File lifecycle:
        # -> source (downloaded local file)
        # -> preprocessed (extracted speeches file)
        # -> converted (actual inference result)
        # -> target (restored speeches file)
        self._source_path = source_path
        self._source_file = self._storage.get_file(source_path)
        self._preprocessed_file = None
        self._converted_file = None
        self._target_file_local_path = None
        self._target_file_remote_path = None

        self._ap = None
        self._auto_pitch_correction_semitones = None
        self._cached_source = []

    @property
    def target_file_remote_path(self):
        return self._target_file_remote_path

    @property
    def auto_pitch_correction_semitones(self):
        return self._auto_pitch_correction_semitones

    @property
    def input_audio_f0m(self):
        return self._ap.joined_speeches_audio_f0m if self._ap else None

    @property
    def storage(self) -> Storage:
        return self._storage

    @property
    def source_path(self) -> str:
        return self._source_path

    @property
    def model(self) -> Model:
        return self._model

    @model.setter
    def model(self, new_model: Model) -> None:
        self._model = new_model

    def preprocess(self):
        # bypass usual preprocessing if we already did it for this source file path
        if self._source_path in self._cached_source:
            if self._bypass_auto_pitch is True:
                # we can't skip validation for the same source file + music mode because the model will be new each time
                AudioFileValidator.validate(self._source_file, self._bypass_auto_pitch, self._model.f0max)
            else:
                # we need to calculate auto pitch correction for each new model instance
                self._auto_pitch_correction_semitones = self._ap.get_auto_pitch_correction(self._model.f0m)
        # usual preprocessing
        else:
            AudioFileValidator.validate(self._source_file, self._bypass_auto_pitch, self._model.f0max)
            self._ap = AudioProcessing(self._source_file, self._processing_mode)
            self._preprocessed_file = self._ap.preprocess()
            AudioFileValidator.check_duration(self._preprocessed_file)
            if self._bypass_auto_pitch is True:
                self._auto_pitch_correction_semitones = 0
            else:
                self._auto_pitch_correction_semitones = self._ap.get_auto_pitch_correction(self._model.f0m)
            # put the source file path to the temp cached list, so we will not preprocess it twice
            self._cached_source.append(self._source_path)
        return self

    def infer(self):
        inf = Inference(
            f0method=self._f0method,
            f0up_key=self._f0up_key,
            filter_radius=self._filter_radius,
            index_rate=self._index_rate,
            input_audio_path=self._preprocessed_file,
            model=self._model,
            protect=self._protect,
            resample_sr=self._resample_sr,
            rms_mix_rate=self._rms_mix_rate,
            auto_pitch_correction_semitones=self._auto_pitch_correction_semitones,
        )
        # remove converted local file if it exists from previous conversion
        if self._converted_file and os.path.isfile(self._converted_file):
            os.remove(self._converted_file)

        self._converted_file = inf.do_inference()
        return self

    def postprocess(self):
        # remove target local file if it exists from previous conversion
        if self._target_file_local_path and os.path.isfile(self._target_file_local_path):
            os.remove(self._target_file_local_path)

        self._target_file_local_path = self._ap.postprocess(self._converted_file)
        self._target_file_remote_path = (AudioProcessingUtils
                                         .get_unique_target_file_remote_path(self._source_path,
                                                                             self._model.name,
                                                                             self._f0up_key,
                                                                             self._bypass_auto_pitch))
        self._storage.put_file(self._target_file_local_path, self._target_file_remote_path)
        return self

    def cleanup(self):
        for file in (self._source_file, self._preprocessed_file, self._converted_file, self._target_file_local_path):
            if file and os.path.isfile(file):
                os.remove(file)

        self._source_file = None
        self._preprocessed_file = None
        self._converted_file = None
        self._target_file_local_path = None
        self._cached_source = []
        return self
