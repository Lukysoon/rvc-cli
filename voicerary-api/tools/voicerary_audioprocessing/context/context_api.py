from tools.voicerary_audioprocessing.context import Context
from tools.voicerary_audioprocessing.model import ModelFactory
from tools.voicerary_audioprocessing.validator import EnvValidator, PayloadValidator


class ContextApi(Context):

    def __init__(self, payload: dict):
        EnvValidator.validate(self.REQUIRED_ENV_VARS[self.API])
        PayloadValidator.validate(payload)

        models = ModelFactory.from_cf_worker(is_model_file_required=False)

        super().__init__(Context.API, payload, models)
