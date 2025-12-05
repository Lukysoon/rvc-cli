from abc import ABC, abstractmethod


class Storage(ABC):
    LOG_RESPONSE = 'response'
    LOG_ERROR = 'error'
    LOG_FILE_NAME_TEMPLATE = "{base}/{log_type}/{date}_{log_type}_{env}_{id}.json"
    LOG_INPUT_FILE_NAME_TEMPLATE = "{base}/{log_type}/{date}_{log_type}_{env}_{id}_{input_file}"

    def __init__(self):
        self._local_path = None

    @abstractmethod
    def get_file(self, src_path: str) -> str:
        pass

    @abstractmethod
    def put_file(self, src_path: str, dst_path: str) -> None:
        pass

    @abstractmethod
    def save_log(self, log_type: str, job_id: str, data: dict) -> None:
        pass

    def cleanup(self):
        pass

    @staticmethod
    def emergency_log_storage():
        pass
