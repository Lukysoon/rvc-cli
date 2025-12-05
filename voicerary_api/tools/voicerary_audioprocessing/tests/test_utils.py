import os
import tempfile
from unittest.mock import patch, mock_open

from tools.voicerary_audioprocessing.utils import AudioProcessingUtils


def test_get_temp_file_path():
    path = AudioProcessingUtils.get_temp_file_path('test.txt')
    assert path == os.path.join(tempfile.gettempdir(), 'test.txt')


def test_append_to_temp_file(monkeypatch):
    mock_open_instance = mock_open()
    monkeypatch.setattr("builtins.open", mock_open_instance)
    AudioProcessingUtils.append_to_temp_file('test.txt', 'test line')
    mock_open_instance().write.assert_called_once_with('test line')


@patch('os.remove')
@patch('glob.glob')
def test_remove_temp_files(mock_glob, mock_remove):
    mock_glob.return_value = ['temp1', 'temp2']
    AudioProcessingUtils.remove_temp_files('*.tmp')
    assert mock_remove.call_count == 2


def test_semitone_distance():
    assert AudioProcessingUtils.semitone_distance(440, 220) == 12
