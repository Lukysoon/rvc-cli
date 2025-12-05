import pytest

from tools.voicerary_audioprocessing import Context
from tools.voicerary_audioprocessing.validator.env_validator import EnvValidator
from tools.voicerary_audioprocessing.voicerary_exception import VoiceraryException


# Create a fixture for preparing environment variables
@pytest.fixture
def prepare_env_vars(monkeypatch):
    monkeypatch.setenv("APP_ENV", "value")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "value")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "value")
    monkeypatch.setenv("CF_ACCOUNT_ID", "value")
    monkeypatch.setenv("INDEX_ROOT", "value")
    monkeypatch.setenv("MODELS_ACCESS_KEY_ID", "value")
    monkeypatch.setenv("MODELS_BUCKET", "value")
    monkeypatch.setenv("MODELS_SECRET_ACCESS_KEY", "value")
    monkeypatch.setenv("VC_BUCKET", "value")
    monkeypatch.setenv("WEIGHT_ROOT", "value")


# Use fixture in the test
def test_env_vars_set(prepare_env_vars, monkeypatch):
    assert EnvValidator.validate(Context.REQUIRED_ENV_VARS[Context.API]) == True


# Use fixture in the test
def test_missing_env_var_raises_exception(prepare_env_vars, monkeypatch):
    monkeypatch.delenv("AWS_SECRET_ACCESS_KEY")

    with pytest.raises(VoiceraryException):
        EnvValidator.validate(Context.REQUIRED_ENV_VARS[Context.API])
