import logging
import os
import time

from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

from tools.voicerary_audioprocessing.error_messages import INTERNAL_ERR_MESSAGES, ERR_INVALID_MODEL_GENDER, \
    USER_FRIENDLY_ERR_MESSAGES, ERR_INVALID_MODEL_AGE, ERR_MODEL_NOT_FOUND
from tools.voicerary_audioprocessing.voicerary_exception import VoiceraryException


class Model:
    MALE = "male"
    FEMALE = "female"
    GENDERS = (MALE, FEMALE)

    CHILD = "child"
    YOUNG = "young"
    MID = "mid"
    OLDER = "older"
    AGES = (CHILD, YOUNG, MID, OLDER)

    def __init__(self,
                 name: str,
                 language: str,
                 age: str,
                 gender: str,
                 f0m: float,
                 f0max: float,
                 models_bucket,
                 image: str = '',
                 is_model_file_required: bool = False,
                 ):
        if gender not in self.GENDERS:
            raise VoiceraryException(INTERNAL_ERR_MESSAGES[ERR_INVALID_MODEL_GENDER].format(gender=gender),
                                     USER_FRIENDLY_ERR_MESSAGES[ERR_INVALID_MODEL_GENDER])

        if age not in self.AGES:
            raise VoiceraryException(INTERNAL_ERR_MESSAGES[ERR_INVALID_MODEL_AGE].format(age=age),
                                     USER_FRIENDLY_ERR_MESSAGES[ERR_INVALID_MODEL_AGE])

        self.name = name
        self.language = language
        self.age = age
        self.gender = gender
        self.f0m = f0m
        self.f0max = f0max
        self.image = image
        self._models_bucket = models_bucket

        if is_model_file_required:
            self.find_model_path()
            self.find_model_index()
        else:
            self.model_path = ''
            self.index_path = ''

    def find_model_path(self) -> str:
        model_file = f'{self.name}.pth'
        model_local_path = os.path.join(os.getenv("WEIGHT_ROOT"), model_file)
        if not os.path.isfile(model_local_path):
            start_time = time.time()
            logger.info(f'START DOWNLOAD MODEL: {model_file}')
            self._models_bucket.download_file(f'models/{model_file}', model_local_path)
            logger.info(f'END DOWNLOAD MODEL: {model_file}. IT TOOK {round(time.time() - start_time, 3)} SECONDS TO COMPLETE')
            if not os.path.isfile(model_local_path):
                raise VoiceraryException(INTERNAL_ERR_MESSAGES[ERR_MODEL_NOT_FOUND].format(model=model_file),
                                         USER_FRIENDLY_ERR_MESSAGES[ERR_MODEL_NOT_FOUND])
        self.model_path = model_local_path
        return self.model_path

    def find_model_index(self) -> str:
        index_file = f'{self.name}.index'
        index_local_path = os.path.join(os.getenv("INDEX_ROOT"), index_file)
        if not os.path.isfile(index_local_path):
            try:
                self._models_bucket.download_file(f'models/{index_file}', index_local_path)
            except ClientError as e:
                if e.response["Error"]["Code"] == '404':
                    # it is fine if there is no index file, that could happen
                    pass

        self.index_path = index_local_path if os.path.isfile(index_local_path) else ''
        return self.index_path
