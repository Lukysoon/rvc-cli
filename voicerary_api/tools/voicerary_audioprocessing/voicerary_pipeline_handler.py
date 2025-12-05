import time
import traceback
import logging

from tools.voicerary_audioprocessing import Context, Storage, VoiceraryPipeline, AudioProcessingUtils
from tools.voicerary_audioprocessing.error_messages import USER_FRIENDLY_ERR_MESSAGES, ERR_GENERAL
from tools.voicerary_audioprocessing.model import Model
from tools.voicerary_audioprocessing.voicerary_exception import VoiceraryException

logger = logging.getLogger(__name__)

class VoiceraryPipelineHandler:

    def __init__(self, ctx: Context, storage: Storage):
        self.context = ctx
        self.storage = storage
        self._pipeline = None
        self._job_status = []

    def process(self):
        pipeline = None
        files = self._get_file_list_from_payload()
        models = self._get_model_list_from_payload()
        for file_name in files:
            for model_name in models:
                try:
                    start_time = time.time()
                    logger.info(f'{self.context.id}: START GET MODEL: {model_name}')
                    model = self.context.get_model_instance_by_name(model_name)
                    logger.info(f'{self.context.id}: END GET MODEL: {model_name}. IT TOOK {round(time.time() - start_time, 3)} SECONDS TO COMPLETE')

                    start_time = time.time()
                    logger.info(f'{self.context.id}: START GET PIPELINE INSTANCE')
                    pipeline = self._get_pipeline(model, file_name)
                    logger.info(f'{self.context.id}: END GET PIPELINE INSTANCE. IT TOOK {round(time.time() - start_time, 3)} SECONDS TO COMPLETE')

                    start_time = time.time()
                    logger.info(f'{self.context.id}: START PREPROCESS')
                    pipeline = pipeline.preprocess()
                    logger.info(f'{self.context.id}: END PREPROCESS. IT TOOK {round(time.time() - start_time, 3)} SECONDS TO COMPLETE')

                    start_time = time.time()
                    logger.info(f'{self.context.id}: START INFERENCE')
                    pipeline = pipeline.infer()
                    logger.info(f'{self.context.id}: END INFERENCE. IT TOOK {round(time.time() - start_time, 3)} SECONDS TO COMPLETE')

                    start_time = time.time()
                    logger.info(f'{self.context.id}: START POSTPROCESS')
                    pipeline = pipeline.postprocess()
                    logger.info(f'{self.context.id}: END POSTPROCESS. IT TOOK {round(time.time() - start_time, 3)} SECONDS TO COMPLETE')
                except (VoiceraryException, Exception) as e:
                    error_message = e.user_message if isinstance(e, VoiceraryException) \
                        else USER_FRIENDLY_ERR_MESSAGES[ERR_GENERAL]

                    self._job_status.append({
                        "model": model_name,
                        "input_file": file_name,
                        "input_f0m": pipeline.input_audio_f0m if pipeline else None,
                        "auto_pitch_correction_semitones": pipeline.auto_pitch_correction_semitones if pipeline else None,
                        "output_file": None,
                        "status": AudioProcessingUtils.PROCESSING_ERROR,
                        "error_message": error_message,
                        "error_details": str(e),
                        "traceback": traceback.format_exc().splitlines()
                    })
                else:
                    self._job_status.append({
                        "model": model_name,
                        "input_file": file_name,
                        "input_f0m": pipeline.input_audio_f0m,
                        "auto_pitch_correction_semitones": pipeline.auto_pitch_correction_semitones,
                        "output_file": pipeline.target_file_remote_path,
                        "status": AudioProcessingUtils.PROCESSING_SUCCESS,
                        "error_message": None,
                        "error_details": None,
                        "traceback": None,
                    })
                finally:
                    # cleanup pipeline files every time for single and batch modes
                    if pipeline and self.context.processing_mode in [Context.MODE_SINGLE, Context.MODE_BATCH]:
                        pipeline.cleanup()

        # do final cleanup
        if pipeline and self.context.processing_mode in [Context.MODE_PREVIEW, Context.MODE_MULTI]:
            pipeline.cleanup()

        if not self._check_overall_job_processing_success():
            raise VoiceraryException(log_message=self._job_status[0]["error_details"],
                                     user_message=self._job_status[0]["error_message"],
                                     orig_traceback=self._job_status[0]["traceback"])

    def processing_result(self):
        return AudioProcessingUtils.handle_response(self.context.payload,
                                                    self.storage,
                                                    self._job_status)

    def _check_overall_job_processing_success(self):
        # if at least one conversion was successful, return normal response and show status for each file/model pair
        return any(item.get('status') == AudioProcessingUtils.PROCESSING_SUCCESS for item in self._job_status)

    def _get_file_list_from_payload(self) -> tuple:
        files = self.context.get_payload_by_key('filepath')
        if isinstance(files, list):
            return tuple(files)
        else:
            return (files,)

    def _get_model_list_from_payload(self) -> tuple:
        models = self.context.get_payload_by_key('model_name')
        if isinstance(models, list):
            return tuple(models)
        else:
            return (models,)

    def _get_pipeline(self, model: Model, file_name: str) -> VoiceraryPipeline:
        # reuse existing pipeline if source file path remains the same (preview and multi modes)
        if self._pipeline and self._pipeline.source_path == file_name \
                and self.context.processing_mode in [Context.MODE_PREVIEW, Context.MODE_MULTI]:
            self._pipeline.model = model
        else:
            # make sure to clean up old pipeline files before creating a new one
            if self._pipeline:
                self._pipeline.cleanup()
            self._pipeline = VoiceraryPipeline(model=model,
                                               storage=self.storage,
                                               source_path=file_name,
                                               processing_mode=self.context.processing_mode,
                                               f0method=self.context.get_payload_by_key('f0method'),
                                               f0up_key=self.context.get_payload_by_key('f0up_key'),
                                               filter_radius=self.context.get_payload_by_key('filter_radius'),
                                               index_rate=self.context.get_payload_by_key('index_rate'),
                                               protect=self.context.get_payload_by_key('protect'),
                                               resample_sr=self.context.get_payload_by_key('resample_sr'),
                                               rms_mix_rate=self.context.get_payload_by_key('rms_mix_rate'),
                                               bypass_auto_pitch=self.context.get_payload_by_key('bypass_auto_pitch')
                                               )
        return self._pipeline
