from unittest.mock import mock_open

import pytest

from tools.voicerary_audioprocessing.storage.local_storage import LocalStorage  # this might differ based on your module
from tools.voicerary_audioprocessing.voicerary_exception import VoiceraryException


@pytest.fixture
def mock_isdir(mocker):
    return mocker.patch("os.path.isdir", return_value=True)


@pytest.fixture
def mock_access(mocker):
    return mocker.patch("os.access", return_value=True)


@pytest.fixture
def mock_temp(mocker):
    return mocker.patch("tempfile.mkdtemp")


@pytest.fixture
def storage(mock_isdir, mock_access, mock_temp):
    return LocalStorage(storage_root="test_dir")


def test_init(mock_isdir, mock_access, mock_temp):
    storage = LocalStorage(storage_root="test_dir")
    assert storage._keep is True


def test_get_file(mocker, storage):
    mock_mkstemp = mocker.patch("tempfile.mkstemp", return_value=(0, "tmp_dst"))
    mock_copy = mocker.patch("shutil.copyfile", return_value="tmp_dst")
    res = storage.get_file("src_path")
    mock_copy.assert_called_once_with("src_path", "tmp_dst")
    assert res == "tmp_dst"


def test_put_file(mocker, storage):
    mock_exists = mocker.patch("os.path.exists", return_value=True)
    mock_makedirs = mocker.patch("os.makedirs")
    mock_copy = mocker.patch("shutil.copy")
    storage.put_file("src_path", "dst_path")
    mock_copy.assert_called_once_with("src_path", "dst_path")


def test_put_file_error(storage):
    with pytest.raises(VoiceraryException):
        storage.put_file("src_path", "dst_path")


def test_save_log(mocker, storage):
    mock_open_fn = mocker.patch("builtins.open", new_callable=mock_open)
    mock_getenv = mocker.patch("os.getenv", return_value="env")
    storage.save_log("log_type", "job_id", {"content": "log"})
    mock_open_fn.assert_called_once()  # checks if file write happened
