import traceback
import uuid

from dotenv import load_dotenv

from tools.voicerary_audioprocessing.error_messages import USER_FRIENDLY_ERR_MESSAGES, ERR_GENERAL
from tools.voicerary_audioprocessing.voicerary_exception import VoiceraryException

load_dotenv()

from tools.voicerary_audioprocessing import *


def process(job: dict):
    vc_handler = None
    try:
        ctx = ContextStandalone(job)
        storage = LocalStorage()
        vc_handler = VoiceraryPipelineHandler(ctx, storage)
        vc_handler.process()
    except (VoiceraryException, Exception) as e:
        err_response = (AudioProcessingUtils
                        .handle_exception(payload=job,
                                          err_message=str(e),
                                          err_message_for_user=e.user_message if isinstance(e, VoiceraryException) else
                                          USER_FRIENDLY_ERR_MESSAGES[ERR_GENERAL],
                                          traceback=e.orig_traceback if (
                                                  hasattr(e, "orig_traceback") and e.orig_traceback)
                                          else traceback.format_exc().splitlines(),
                                          storage=vc_handler.storage if vc_handler else None,
                                          ))
        return err_response
    else:
        return vc_handler.processing_result()


if __name__ == '__main__':
    job = {
        "id": str(uuid.uuid4()),
        "input": {
            "mode": "preview",
            "bypass_auto_pitch": True,
            "f0method": "rmvpe",
            "f0up_key": 0,
            "filepath": [
                "/Users/roman/Downloads/test/K_6.aif"
            ],
            "filter_radius": 3,
            "index_rate": 0,
            "model_name": [
                "Jakub"
            ],
            "protect": 0.1,
            "resample_sr": 0,
            "rms_mix_rate": 1
        }
    }
    process(job)
