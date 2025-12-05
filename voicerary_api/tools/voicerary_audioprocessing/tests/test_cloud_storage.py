import os
import tempfile

import pytest
from tools.voicerary_audioprocessing import CloudStorage
from tools.voicerary_audioprocessing.voicerary_exception import VoiceraryException


@pytest.fixture
def cloud_storage(mocker):
    mock_bucket = mocker.Mock()
    mock_resource = mocker.Mock()
    mock_resource.Bucket.return_value = mock_bucket
    bucket = "test_bucket"
    cloud_storage = CloudStorage(mock_resource, bucket)
    test_file_path = os.path.join(tempfile.gettempdir(), "test_file.txt")
    yield cloud_storage, test_file_path
    if os.path.exists(test_file_path):
        os.remove(test_file_path)


def test_get_file(cloud_storage):
    cloud_storage, test_file_path = cloud_storage
    with open(test_file_path, "w") as file:
        file.write("Test file content")

    result_path = cloud_storage.get_file(test_file_path)
    assert result_path == test_file_path
    cloud_storage._resource.Bucket.assert_called_once_with("test_bucket")
    cloud_storage._resource.Bucket.return_value.download_file.assert_called_once_with(test_file_path, test_file_path)


def test_get_file_no_local_file(cloud_storage):
    cloud_storage, test_file_path = cloud_storage

    with pytest.raises(VoiceraryException):
        cloud_storage.get_file("non_existent_file_path")


def test_put_file(cloud_storage):
    cloud_storage, test_file_path = cloud_storage
    with open(test_file_path, "w") as file:
        file.write("Test file content")
    dst_file_path = "dst_file_path"

    assert cloud_storage.put_file(test_file_path, dst_file_path)
    cloud_storage._resource.Bucket.assert_called_once_with("test_bucket")
    cloud_storage._resource.Bucket.return_value.upload_file.assert_called_once_with(test_file_path, dst_file_path)


def test_put_file_no_local_file(cloud_storage):
    cloud_storage, _ = cloud_storage
    dst_file_path = "dst_file_path"

    with pytest.raises(VoiceraryException):
        cloud_storage.put_file("non_existent_file_path", dst_file_path)


def test_save_log(cloud_storage):
    cloud_storage, test_file_path = cloud_storage
    with open(test_file_path, "w") as file:
        file.write("Test file content")

    cloud_storage.save_log("TEST_TYPE", "JOB_ID", {})

    assert cloud_storage._resource.Bucket.called
    assert cloud_storage._resource.Bucket.return_value.upload_file.called
