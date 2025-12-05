import json
import os
import unittest
from unittest.mock import patch, mock_open, MagicMock

from tools.voicerary_audioprocessing.error_messages import ERR_FILE_NOT_EXISTS, ERR_FILE_IS_NOT_READABLE, \
    ERR_INVALID_MODEL_METADATA_FILE
from tools.voicerary_audioprocessing.model import Model
from tools.voicerary_audioprocessing.model.model_factory import ModelFactory
from tools.voicerary_audioprocessing.voicerary_exception import VoiceraryException


class TestModelFactory(unittest.TestCase):

    @patch('os.path.isfile', return_value=False)
    def test_json_file_not_exists(self, mock_isfile):
        with self.assertRaises(VoiceraryException) as context:
            ModelFactory.from_json_file('not_exists.json')
            self.assertTrue(ERR_FILE_NOT_EXISTS in str(context.exception))

    @patch('os.path.isfile', return_value=True)
    @patch('os.access', return_value=False)
    def test_json_file_inaccessible(self, mock_access, mock_isfile):
        with self.assertRaises(VoiceraryException) as context:
            ModelFactory.from_json_file('inaccessible.json')
            self.assertTrue(ERR_FILE_IS_NOT_READABLE in str(context.exception))

    @patch('os.path.isfile', return_value=True)
    @patch('os.access', return_value=True)
    def test_json_file_invalid_content(self, mock_access, mock_isfile):
        with patch('builtins.open', mock_open(read_data='invalid: json: - here')):
            with self.assertRaises(VoiceraryException) as context:
                ModelFactory.from_json_file('invalid.json')
                self.assertTrue(ERR_INVALID_MODEL_METADATA_FILE in str(context.exception))

    @patch('os.path.isfile', return_value=True)
    @patch('os.access', return_value=True)
    def test_json_file_valid(self, mock_access, mock_isfile):
        test_data = [
            {
                "name": "model1",
                "language": "en",
                "gender": "male",
                "age": "young",
                "image": "model1.jpg",
                "f0m": 120,
                "f0max": 200
            }
        ]
        test_data_json = json.dumps(test_data)

        with patch('builtins.open', mock_open(read_data=test_data_json)):
            result = ModelFactory.from_json_file('valid.json')
            self.assertIsInstance(result["model1"], Model)
            self.assertEqual(result["model1"].f0max, 200)

    @patch('httpx.get')
    def test_from_cf_worker_no_file_required(self, mock_get):
        # Arrange
        os.environ['MODELS_METADATA_URL'] = 'http://test.com'
        os.environ['CF_DB_WORKER_API_TOKEN'] = 'test_token'
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [
            {
                "name": "model1",
                "language": "en",
                "gender": "male",
                "age": "young",
                "image": "model1.jpg",
                "f0m": 120,
                "f0max": 200
            }
        ]
        mock_get.return_value = mock_response

        # Act
        result = ModelFactory.from_cf_worker(False)

        # Assert
        mock_get.assert_called_once_with(os.getenv('MODELS_METADATA_URL'),
                                         headers={'Authorization': f"Bearer {os.getenv('CF_DB_WORKER_API_TOKEN')}"})
        self.assertIsInstance(result["model1"], Model)
        self.assertEqual(result["model1"].f0max, 200)

        # Assert
        mock_get.assert_called_once_with(os.getenv('MODELS_METADATA_URL'),
                                         headers={'Authorization': f"Bearer {os.getenv('CF_DB_WORKER_API_TOKEN')}"})
        self.assertIsInstance(result["model1"], Model)
        self.assertEqual(result["model1"].f0max, 200)
