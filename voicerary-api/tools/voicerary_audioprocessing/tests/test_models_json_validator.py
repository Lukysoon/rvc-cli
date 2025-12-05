import pytest
from tools.voicerary_audioprocessing.validator import ModelsJsonValidator
from tools.voicerary_audioprocessing.voicerary_exception import VoiceraryException


def test_validate():

    valid_payload = [{
        "name": "John Doe",
        "language": "English",
        "gender": "male",
        "age": "young",
        "image": "https://example.com/image.jpg",
        "f0m": 0.3,
        "f0max": 0.5
    }]

    assert ModelsJsonValidator.validate(valid_payload)

    invalid_payload = [{
        "name": 123,
        "language": "English",
        "gender": "male",
        "age": "young",
        "image": "https://example.com/image.jpg",
        "f0m": "invalid_float",
        "f0max": 0.5
    }]

    with pytest.raises(VoiceraryException):
        ModelsJsonValidator.validate(invalid_payload)

    missing_value_payload = [{
        "name": "John Doe",
        "language": "English",
        "f0m": 0.3,
        "f0max": 0.5
    }]

    with pytest.raises(VoiceraryException):
        ModelsJsonValidator.validate(missing_value_payload)

    extra_value_payload = [{
        "name": "John Doe",
        "language": "English",
        "gender": "male",
        "age": "young",
        "image": "https://example.com/image.jpg",
        "f0m": 0.3,
        "f0max": 0.5,
        "extra": "extra_value"
    }]

    assert ModelsJsonValidator.validate(valid_payload)
