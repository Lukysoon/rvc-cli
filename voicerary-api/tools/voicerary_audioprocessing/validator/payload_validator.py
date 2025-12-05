import jsonschema
from jsonschema import validate

from tools.voicerary_audioprocessing.error_messages import INTERNAL_ERR_MESSAGES, ERR_INVALID_PAYLOAD, \
    USER_FRIENDLY_ERR_MESSAGES
from tools.voicerary_audioprocessing.voicerary_exception import VoiceraryException


class PayloadValidator:
    REQUEST_SCHEMA = {
        "type": "object",
        "properties": {
            "id": {
                "type": "string"
            },
            "input": {
                "type": "object",
                "properties": {
                    "bypass_auto_pitch": {
                        "type": "boolean"
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["single", "preview", "batch", "multi"]
                    },
                    "f0method": {
                        "type": "string",
                        "enum": ["rmvpe"]
                    },
                    "f0up_key": {
                        "type": "integer",
                        "minimum": -18,
                        "maximum": 18
                    },
                    "filepath": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "filter_radius": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 7
                    },
                    "index_rate": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1
                    },
                    "model_name": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "protect": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 0.5
                    },
                    "resample_sr": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 48000
                    },
                    "rms_mix_rate": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1
                    }
                },
                "required": ["bypass_auto_pitch",
                             "mode",
                             "f0method",
                             "f0up_key",
                             "filepath",
                             "filter_radius",
                             "index_rate",
                             "model_name",
                             "protect",
                             "resample_sr",
                             "rms_mix_rate"]
            },
        },
        "required": ["id", "input"]
    }

    @staticmethod
    def validate(payload: dict) -> bool:
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
            validate(instance=payload, schema=PayloadValidator.REQUEST_SCHEMA)
            if payload["input"]["mode"] == "single" \
                    and (len(payload["input"]["filepath"]) != 1
                         or len(payload["input"]["model_name"]) != 1):
                raise jsonschema.exceptions.ValidationError(
                    "One model and one file are required for mode 'single'")

            if payload["input"]["mode"] == "preview" \
                    and (len(payload["input"]["filepath"]) != 1
                         or len(payload["input"]["model_name"]) < 1 or len(payload["input"]["model_name"]) > 300):
                raise jsonschema.exceptions.ValidationError(
                    "One file and at least one model (but not more 300) are required for mode 'preview'")

            if payload["input"]["mode"] == "batch" \
                    and (len(payload["input"]["filepath"]) <= 1 or len(payload["input"]["filepath"]) > 100
                         or len(payload["input"]["model_name"]) != 1):
                raise jsonschema.exceptions.ValidationError(
                    "One model and multiple files (but not more 100) are required for mode 'batch'")

            if payload["input"]["mode"] == "multi" \
                    and (len(payload["input"]["filepath"]) <= 1 or len(payload["input"]["filepath"]) > 20
                         or len(payload["input"]["model_name"]) <= 1 or len(payload["input"]["model_name"]) > 20):
                raise jsonschema.exceptions.ValidationError(
                    "Multiple files and models are required for mode 'multi'. Max 20 files and 20 models (400 conversions per request)")

        except (jsonschema.exceptions.ValidationError, jsonschema.exceptions.SchemaError) as e:
            raise VoiceraryException(INTERNAL_ERR_MESSAGES[ERR_INVALID_PAYLOAD].format(err=str(e)),
                                     USER_FRIENDLY_ERR_MESSAGES[ERR_INVALID_PAYLOAD])

        return True
