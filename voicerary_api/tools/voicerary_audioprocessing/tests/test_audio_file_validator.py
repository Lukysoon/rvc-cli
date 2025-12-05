from unittest.mock import patch

import pytest

from tools.voicerary_audioprocessing.validator.audio_file_validator import AudioFileValidator
from tools.voicerary_audioprocessing.voicerary_exception import VoiceraryException


@patch('ffmpeg.probe')
@patch('os.path.isfile')
def test_validate(mock_isfile, mock_probe):
    mock_isfile.return_value = True
    mock_probe.return_value = {
        'streams': [{'codec_type': 'audio'}],
        'format': {'duration': 3600}
    }
    with (patch.object(AudioFileValidator, '_rms_level', return_value=-35), \
          patch.object(AudioFileValidator, '_has_suitable_pitch', return_value=True)):
        assert AudioFileValidator.validate('path_to_audio_file', True, 500)


@patch('os.path.isfile')
def test_validate_file_not_found(mock_isfile):
    mock_isfile.return_value = False
    with pytest.raises(VoiceraryException):
        AudioFileValidator.validate('path_to_non_existent_file', True, 500)


@patch('ffmpeg.probe', side_effect=Exception)
@patch('os.path.isfile')
def test_ffprobe_error(mock_isfile, mock_probe):
    mock_isfile.return_value = True
    with pytest.raises(Exception):
        AudioFileValidator.validate('path_to_invalid_file', True, 500)
