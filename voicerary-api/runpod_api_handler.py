import time
import traceback
import logging

import runpod
from dotenv import load_dotenv

from tools.voicerary_audioprocessing.error_messages import USER_FRIENDLY_ERR_MESSAGES, ERR_GENERAL
from tools.voicerary_audioprocessing.voicerary_exception import VoiceraryException

load_dotenv()

logger = logging.getLogger(__name__)

from tools.voicerary_audioprocessing import *


def process(job: dict):
    start_time = time.time()
    logger.info(f'START PROCESSING JOB: {job["id"]}')
    vc_handler = None
    try:
        ctx = ContextApi(job)
        storage = CloudStorage()
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
    finally:
        logger.info(f'END PROCESSING JOB: {job["id"]}. IT TOOK {round(time.time() - start_time, 3)} SECONDS TO COMPLETE')


runpod.serverless.start({"handler": process})
