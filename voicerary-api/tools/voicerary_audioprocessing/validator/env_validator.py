import os

from tools.voicerary_audioprocessing.error_messages import ERR_ENV_VAR_NOT_SET, USER_FRIENDLY_ERR_MESSAGES, \
    INTERNAL_ERR_MESSAGES
from tools.voicerary_audioprocessing.voicerary_exception import VoiceraryException


class EnvValidator:

    @staticmethod
    def validate(required_vars: tuple) -> bool:
        """

        :param required_vars:
        :return: bool
        :raises:
                `ValueError`

                if any of required environment variables is not set
        """
        for var in required_vars:
            if var not in os.environ:
                raise VoiceraryException(INTERNAL_ERR_MESSAGES[ERR_ENV_VAR_NOT_SET].format(var=var),
                                         USER_FRIENDLY_ERR_MESSAGES[ERR_ENV_VAR_NOT_SET])

        return True
