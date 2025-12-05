import json
import logging
import os
import tempfile
import time
from datetime import datetime

import boto3
from boto3.s3.transfer import TransferConfig, MB
from botocore.config import Config
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

from tools.voicerary_audioprocessing.error_messages import ERR_GET_FILE_CLOUD, ERR_PUT_FILE_CLOUD, \
    USER_FRIENDLY_ERR_MESSAGES, INTERNAL_ERR_MESSAGES
from .storage import Storage
from ..voicerary_exception import VoiceraryException


class CloudStorage(Storage):
    DEFAULT_LOGS_PATH = 'vc/logs'

    def __init__(self):
        session = boto3.Session(
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        )
        self._resource = session.resource('s3', config=Config(signature_version='s3v4'),
                                          endpoint_url=f'https://{os.getenv("CF_ACCOUNT_ID")}.r2.cloudflarestorage.com')
        self._bucket = os.getenv("VC_BUCKET")
        super().__init__()

    def get_file(self, src_path: str) -> str:
        """

        :param src_path: str, path to the file on remote bucket
        :return: str, local path to the downloaded file
        :raise: Exception if download failed or if there is no local file
        """
        local_path = os.path.join(tempfile.gettempdir(), os.path.basename(src_path))
        try:
            config = TransferConfig(multipart_threshold=2 * MB,
                                    max_concurrency=10,
                                    multipart_chunksize=50 * MB,
                                    use_threads=True)
            start_time = time.time()
            logger.info('START DOWNLOAD AUDIO')
            self._resource.Bucket(self._bucket).download_file(src_path, local_path, Config=config)
            logger.info(f'END DOWNLOAD AUDIO. IT TOOK {round(time.time() - start_time, 3)} SECONDS TO COMPLETE')

        except ClientError as e:
            if e.response["Error"]["Code"] == '404':
                raise VoiceraryException(
                    INTERNAL_ERR_MESSAGES[ERR_GET_FILE_CLOUD].format(src_path=src_path, local_path=local_path),
                    USER_FRIENDLY_ERR_MESSAGES[ERR_GET_FILE_CLOUD])

        if not os.path.isfile(local_path):
            raise VoiceraryException(
                INTERNAL_ERR_MESSAGES[ERR_GET_FILE_CLOUD].format(src_path=src_path, local_path=local_path),
                USER_FRIENDLY_ERR_MESSAGES[ERR_GET_FILE_CLOUD])

        self._local_path = local_path
        return self._local_path

    def put_file(self, src_path: str, dst_path: str) -> bool:
        """

        :param src_path:
        :param dst_path:
        :return: bool, True if there were no exceptions during upload
        :raise: Exception if upload failed or if there is no local file
        """
        if not os.path.isfile(src_path):
            raise VoiceraryException(
                INTERNAL_ERR_MESSAGES[ERR_PUT_FILE_CLOUD].format(dst_path=dst_path, src_path=src_path),
                USER_FRIENDLY_ERR_MESSAGES[ERR_PUT_FILE_CLOUD])

        start_time = time.time()
        logger.info(f'START UPLOAD {src_path} to {dst_path}')
        self._resource.Bucket(self._bucket).upload_file(src_path, dst_path)
        logger.info(f'END UPLOAD to {dst_path}. IT TOOK {round(time.time() - start_time, 3)} SECONDS TO COMPLETE')
        return True

    def save_log(self, log_type: str, job_id: str, data: dict) -> None:
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            current_time = datetime.now()
            data['event_time'] = current_time.isoformat()
            json.dump(data, f, indent=4)
            f.close()
            dst_path = Storage.LOG_FILE_NAME_TEMPLATE.format(date=current_time.strftime("%Y-%m-%d_%H-%M-%S"),
                                                             log_type=log_type,
                                                             env=os.getenv("APP_ENV", "NA"),
                                                             id=job_id,
                                                             base=CloudStorage.DEFAULT_LOGS_PATH,
                                                             )
            self.put_file(f.name, dst_path)
            if log_type == Storage.LOG_ERROR and self._local_path and os.path.isfile(self._local_path):
                #  let's save the original input file if it exists locally, it will help to debug and fix errors
                dst_path = Storage.LOG_INPUT_FILE_NAME_TEMPLATE.format(date=current_time.strftime("%Y-%m-%d_%H-%M-%S"),
                                                                       log_type=log_type,
                                                                       env=os.getenv("APP_ENV", "NA"),
                                                                       id=job_id,
                                                                       input_file=os.path.basename(self._local_path),
                                                                       base=CloudStorage.DEFAULT_LOGS_PATH,
                                                                       )
                self.put_file(self._local_path, dst_path)
            os.remove(f.name)

    @staticmethod
    def emergency_log_storage():
        if os.getenv('AWS_ACCESS_KEY_ID') \
                and os.getenv('AWS_SECRET_ACCESS_KEY') \
                and os.getenv("CF_ACCOUNT_ID") \
                and os.getenv("VC_BUCKET"):
            return CloudStorage()
