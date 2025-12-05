from unittest.mock import patch

import pytest
from tools.voicerary_audioprocessing.voicerary_exception import VoiceraryException
from tools.voicerary_audioprocessing.model import *


@patch('os.path.isfile', return_value=True)
def test_model_init(mock_isfile):
    # setup
    valid_name = "valid_name"
    valid_language = "valid_language"
    valid_age = Model.YOUNG
    valid_gender = Model.MALE
    valid_f0m = 120.0
    valid_f0max = 500.0

    # action
    model = Model(
        name=valid_name,
        language=valid_language,
        age=valid_age,
        gender=valid_gender,
        f0m=valid_f0m,
        f0max=valid_f0max
    )

    # check
    assert model.name == valid_name
    assert model.language == valid_language
    assert model.age == valid_age
    assert model.gender == valid_gender
    assert model.f0m == valid_f0m
    assert model.f0max == valid_f0max
    assert model.image == ''


@pytest.mark.parametrize(
    "invalid_age",
    [
        "invalid_age",
        123,
        None,
    ],
)
def test_model_init_invalid_age(invalid_age):
    with pytest.raises(VoiceraryException):
        Model(
            name="valid_name",
            language="valid_language",
            age=invalid_age,
            gender=Model.MALE,
            f0m=120.0,
            f0max=500.0
        )


@pytest.mark.parametrize(
    "invalid_gender",
    [
        "invalid_gender",
        123,
        None,
    ],
)
def test_model_init_invalid_gender(invalid_gender):
    with pytest.raises(VoiceraryException):
        Model(
            name="valid_name",
            language="valid_language",
            age=Model.MID,
            gender=invalid_gender,
            f0m=120.0,
            f0max=500.0
        )
