from abc import ABC

from tools.voicerary_audioprocessing.error_messages import ERR_PAYLOAD_KEY_NOT_EXISTS, ERR_INVALID_CONTEXT, \
    USER_FRIENDLY_ERR_MESSAGES, INTERNAL_ERR_MESSAGES, ERR_MODEL_NOT_FOUND, ERR_INVALID_PROCESSING_MODE
from tools.voicerary_audioprocessing.model import Model
from tools.voicerary_audioprocessing.voicerary_exception import VoiceraryException


class Context(ABC):
    API = 'api'
    STANDALONE = 'standalone'
    VALID_CONTEXT = (API, STANDALONE)
    REQUIRED_ENV_VARS = {
        API: (
            "APP_ENV",
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "CF_ACCOUNT_ID",
            "CF_DB_WORKER_API_TOKEN",
            "INDEX_ROOT",
            "MODELS_ACCESS_KEY_ID",
            "MODELS_BUCKET",
            "MODELS_METADATA_URL",
            "MODELS_SECRET_ACCESS_KEY",
            "RMVPE_ROOT",
            "VC_BUCKET",
            "WEIGHT_ROOT",
            # "MODELS_METADATA_FILE",
        ),
        STANDALONE: (
            "APP_ENV",
            "CF_DB_WORKER_API_TOKEN",
            "INDEX_ROOT",
            "MODELS_ACCESS_KEY_ID",
            "MODELS_BUCKET",
            "MODELS_METADATA_URL",
            "MODELS_SECRET_ACCESS_KEY",
            "RMVPE_ROOT",
            "WEIGHT_ROOT",
            # "MODELS_METADATA_FILE",
        )
    }

    MODE_SINGLE = 'single'
    MODE_PREVIEW = 'preview'
    MODE_BATCH = 'batch'
    MODE_MULTI = 'multi'
    VALID_PROCESSING_MODE = (MODE_SINGLE, MODE_PREVIEW, MODE_BATCH, MODE_MULTI)

    def __init__(self, context: str, payload: dict, models: dict):
        self._payload = payload
        self._ctx_id = payload["id"]

        if context not in Context.VALID_CONTEXT:
            raise VoiceraryException(INTERNAL_ERR_MESSAGES[ERR_INVALID_CONTEXT].format(context=context),
                                     USER_FRIENDLY_ERR_MESSAGES[ERR_INVALID_CONTEXT])

        if self.get_payload_by_key('mode') not in Context.VALID_PROCESSING_MODE:
            raise VoiceraryException(INTERNAL_ERR_MESSAGES[ERR_INVALID_PROCESSING_MODE]
                                     .format(mode=self.get_payload_by_key('mode')),
                                     USER_FRIENDLY_ERR_MESSAGES[ERR_INVALID_PROCESSING_MODE])

        self._processing_mode = self.get_payload_by_key('mode')
        self._context_name = context
        self._models = models

    @property
    def context_name(self):
        return self._context_name

    @property
    def processing_mode(self):
        return self._processing_mode

    @property
    def payload(self):
        return self._payload

    @property
    def id(self):
        return self._ctx_id

    @property
    def models(self):
        return self._models

    def get_model_instance_by_name(self, name: str) -> Model:
        if name not in self._models:
            raise VoiceraryException(INTERNAL_ERR_MESSAGES[ERR_MODEL_NOT_FOUND].format(model=name),
                                     USER_FRIENDLY_ERR_MESSAGES[ERR_MODEL_NOT_FOUND])

        return self._models[name]

    def get_payload_by_key(self, key: str = None):
        if key and key in self._payload["input"]:
            return self._payload["input"][key]
        elif key and key not in self._payload:
            raise VoiceraryException(INTERNAL_ERR_MESSAGES[ERR_PAYLOAD_KEY_NOT_EXISTS].format(key=key),
                                     USER_FRIENDLY_ERR_MESSAGES[ERR_PAYLOAD_KEY_NOT_EXISTS])

        return self._payload
