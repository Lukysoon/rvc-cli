import jsonschema
from jsonschema import validate

from tools.voicerary_audioprocessing.error_messages import INTERNAL_ERR_MESSAGES, ERR_INVALID_PAYLOAD, \
    USER_FRIENDLY_ERR_MESSAGES
from tools.voicerary_audioprocessing.voicerary_exception import VoiceraryException


class ModelsJsonValidator:
    MODELS_SCHEMA = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer"
                },
                "name": {
                    "type": "string"
                },
                "language": {
                    "type": "string"
                },
                "gender": {
                    "type": "string",
                    "enum": ["male", "female"]
                },
                "age": {
                    "type": "string",
                    "enum": ["child", "young", "mid", "older"]
                },
                "image": {
                    "type": "string"
                },
                "f0m": {
                    "type": "number"
                },
                "f0max": {
                    "type": "number"
                },
            },
            "required": ["id", "name", "language", "gender", "age", "f0m", "f0max"]
        }
    }

    @staticmethod
    def validate(payload: list) -> bool:
        """

        :param payload: dict, API request payload
        :return: bool
        :raises:
            `jsonschema.exceptions.ValidationError`:

            if the instance is invalid

            `jsonschema.exceptions.SchemaError`:

            if the schema itself is invalid
        """
        try:
            validate(instance=payload, schema=ModelsJsonValidator.MODELS_SCHEMA)
        except (jsonschema.exceptions.ValidationError, jsonschema.exceptions.SchemaError) as e:
            raise VoiceraryException(INTERNAL_ERR_MESSAGES[ERR_INVALID_PAYLOAD].format(err=str(e)),
                                     USER_FRIENDLY_ERR_MESSAGES[ERR_INVALID_PAYLOAD])

        return True
