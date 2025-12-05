import json
import os.path
import shutil
import tempfile
from datetime import datetime

from .storage import Storage
from ..error_messages import ERR_FILE_NOT_EXISTS, USER_FRIENDLY_ERR_MESSAGES, INTERNAL_ERR_MESSAGES
from ..voicerary_exception import VoiceraryException


class LocalStorage(Storage):
    def __init__(self, storage_root: str = None):
        if storage_root and os.path.isdir(storage_root) and os.access(storage_root, os.W_OK):
            self._storage_root = storage_root
            self._keep = True
        else:
            self._storage_root = tempfile.mkdtemp(prefix='voicerary_standalone_storage_')
            self._keep = False

        self._logs_root = tempfile.mkdtemp(prefix='voicerary_standalone_log_')
        super().__init__()

    def cleanup(self):
        if not self._keep:
            shutil.rmtree(self._storage_root)

    def get_file(self, src_path: str) -> str:
        _, tmp_dst = tempfile.mkstemp(dir=self._storage_root)
        self._local_path = shutil.copyfile(src_path, tmp_dst)
        return self._local_path

    def put_file(self, src_path: str, dst_path: str) -> None:
        if not os.path.exists(src_path):
            raise VoiceraryException(INTERNAL_ERR_MESSAGES[ERR_FILE_NOT_EXISTS].format(file_path=src_path),
                                     USER_FRIENDLY_ERR_MESSAGES[ERR_FILE_NOT_EXISTS])

        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        shutil.copy(src_path, dst_path)

    def save_log(self, log_type: str, job_id: str, data: dict) -> None:
        current_time = datetime.now()
        data['event_time'] = current_time.isoformat()
        dst_path = Storage.LOG_FILE_NAME_TEMPLATE.format(date=current_time.strftime("%Y-%m-%d_%H-%M-%S"),
                                                         log_type=log_type,
                                                         env=os.getenv("APP_ENV", "NA"),
                                                         id=job_id,
                                                         base=self._logs_root,
                                                         )
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        log_file = open(dst_path, 'w')
        json.dump(data, log_file, indent=4)
        log_file.close()
        if log_type == Storage.LOG_ERROR and self._local_path and os.path.isfile(self._local_path):
            #  let's save the original input file if it exists locally, it will help to debug and fix errors
            dst_path = Storage.LOG_INPUT_FILE_NAME_TEMPLATE.format(date=current_time.strftime("%Y-%m-%d_%H-%M-%S"),
                                                                   log_type=log_type,
                                                                   env=os.getenv("APP_ENV", "NA"),
                                                                   id=job_id,
                                                                   input_file=os.path.basename(self._local_path),
                                                                   base=self._logs_root,
                                                                   )
            self.put_file(self._local_path, dst_path)
