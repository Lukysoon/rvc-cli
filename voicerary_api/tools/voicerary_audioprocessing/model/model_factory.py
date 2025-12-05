import json
import logging
import os.path
import time

import boto3
import httpx
from botocore.config import Config
from httpx import Response
from tenacity import retry, wait_exponential, stop_after_attempt

logger = logging.getLogger(__name__)

from tools.voicerary_audioprocessing.error_messages import INTERNAL_ERR_MESSAGES, USER_FRIENDLY_ERR_MESSAGES, \
    ERR_FILE_NOT_EXISTS, ERR_FILE_IS_NOT_READABLE, ERR_INVALID_MODEL_METADATA_FILE, ERR_MODEL_METADATA_API_FETCH
from tools.voicerary_audioprocessing.model.model import Model
from tools.voicerary_audioprocessing.validator.models_json_validator import ModelsJsonValidator
from tools.voicerary_audioprocessing.voicerary_exception import VoiceraryException


class ModelFactory:

    @staticmethod
    def from_json_file(json_file_path: str, is_model_file_required: bool = False) -> dict:
        if not os.path.isfile(json_file_path):
            raise VoiceraryException(INTERNAL_ERR_MESSAGES[ERR_FILE_NOT_EXISTS].format(file_path=json_file_path),
                                     USER_FRIENDLY_ERR_MESSAGES[ERR_FILE_NOT_EXISTS])

        if not os.access(json_file_path, os.R_OK):
            raise VoiceraryException(INTERNAL_ERR_MESSAGES[ERR_FILE_IS_NOT_READABLE].format(file_path=json_file_path),
                                     USER_FRIENDLY_ERR_MESSAGES[ERR_FILE_IS_NOT_READABLE])

        with open(json_file_path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                raise VoiceraryException(INTERNAL_ERR_MESSAGES[ERR_INVALID_MODEL_METADATA_FILE]
                                         .format(file_path=json_file_path),
                                         USER_FRIENDLY_ERR_MESSAGES[ERR_INVALID_MODEL_METADATA_FILE])
            if not data:
                raise VoiceraryException(INTERNAL_ERR_MESSAGES[ERR_INVALID_MODEL_METADATA_FILE]
                                         .format(file_path=json_file_path),
                                         USER_FRIENDLY_ERR_MESSAGES[ERR_INVALID_MODEL_METADATA_FILE])
            ModelsJsonValidator.validate(data)
            return ModelFactory._create_models(data, is_model_file_required)

    @staticmethod
    def from_cf_worker(is_model_file_required: bool = False) -> dict:
        start_time = time.time()
        logger.info('START CF D1 REQUEST')
        r = ModelFactory._get_models_from_cf_worker()
        logger.info(f'END CF D1 REQUEST. IT TOOK {round(time.time() - start_time, 3)} SECONDS TO COMPLETE')

        return ModelFactory._create_models(r.json(), is_model_file_required)

    @staticmethod
    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
    def _get_models_from_cf_worker() -> Response:
        try:
            r = httpx.get(os.getenv('MODELS_METADATA_URL'),
                          headers={'Authorization': f"Bearer {os.getenv('CF_DB_WORKER_API_TOKEN')}"})
            r.raise_for_status()
            return r
        except httpx.HTTPError as exc:
            raise VoiceraryException(INTERNAL_ERR_MESSAGES[ERR_MODEL_METADATA_API_FETCH]
                                     .format(url=exc.request.url,
                                             code=exc.response.status_code if hasattr(exc, 'response') else 500,
                                             message=exc),
                                     USER_FRIENDLY_ERR_MESSAGES[ERR_MODEL_METADATA_API_FETCH])

    @staticmethod
    def _create_models(data: list, is_model_file_required: bool) -> dict:
        models = {}
        ModelsJsonValidator.validate(data)
        models_bucket = ModelFactory._get_models_cloud_storage_bucket()
        for model_data in data:
            model_instance = Model(name=model_data["name"],
                                   language=model_data["language"],
                                   gender=model_data["gender"],
                                   age=model_data["age"],
                                   image=model_data["image"],
                                   f0m=model_data["f0m"],
                                   f0max=model_data["f0max"],
                                   is_model_file_required=is_model_file_required,
                                   models_bucket=models_bucket)
            models[model_data["name"]] = model_instance
        return models

    @staticmethod
    def _get_models_cloud_storage_bucket():
        session = boto3.Session(
            aws_access_key_id=os.getenv('MODELS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('MODELS_SECRET_ACCESS_KEY'),
        )
        resource = session.resource('s3', config=Config(signature_version='s3v4'),
                                    endpoint_url=f'https://{os.getenv("CF_ACCOUNT_ID")}.r2.cloudflarestorage.com')
        bucket = os.getenv("MODELS_BUCKET")
        return resource.Bucket(bucket)
