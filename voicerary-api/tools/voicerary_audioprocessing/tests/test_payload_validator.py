import pytest

from tools.voicerary_audioprocessing.validator.payload_validator import PayloadValidator
from tools.voicerary_audioprocessing.voicerary_exception import VoiceraryException


@pytest.fixture
def payload():
    valid_payload = {
        "id": "uuidv4",
        "input": {
            "bypass_auto_pitch": True,
            "mode": "single",
            "f0method": "rmvpe",
            "f0up_key": 0,
            "filepath": ["path/to/file.aif"],
            "filter_radius": 3,
            "index_rate": 0,
            "model_name": ["Some.Model"],
            "protect": 0.1,
            "resample_sr": 0,
            "rms_mix_rate": 1
        }
    }
    valid_payload_multi_mode = {
        "id": "uuidv4",
        "input": {
            "bypass_auto_pitch": True,
            "mode": "multi",
            "f0method": "rmvpe",
            "f0up_key": 0,
            "filepath": [
                "path/to/file.aif",
                "path/to/file.aif",
                "path/to/file.aif",
            ],
            "filter_radius": 3,
            "index_rate": 0,
            "model_name": [
                "Some.Model1",
                "Some.Model2",
                "Some.Model3",
            ],
            "protect": 0.1,
            "resample_sr": 0,
            "rms_mix_rate": 1
        }
    }
    invalid_payload = {
        "id": "uuidv4",
        "input": {
            "bypass_auto_pitch": "true",  # should be boolean
            "f0method": "rmvpe",
            "mode": 123,
            "f0up_key": 0,
            # "filepath": "path/to/file", # required
            "filter_radius": 0,
            "index_rate": 1.5,  # exceeds maximum value
            "model_name": "test_model",
            "protect": 0.25,
            "resample_sr": 24000,
            "rms_mix_rate": 0.5
        }
    }
    return valid_payload, invalid_payload, valid_payload_multi_mode


def test_validate_valid_payload(payload):
    # Test no exception is raised for a valid payload
    valid_payload, _, _ = payload
    assert PayloadValidator.validate(valid_payload)


def test_validate_invalid_payload(payload):
    # Test ValidationError exception is raised for an invalid payload
    _, invalid_payload, _ = payload
    with pytest.raises(VoiceraryException):
        PayloadValidator.validate(invalid_payload)


def test_validate_valid_payload_multi_mode(payload):
    # Test no exception is raised for a valid payload
    _, _, valid_payload = payload
    assert PayloadValidator.validate(valid_payload)
