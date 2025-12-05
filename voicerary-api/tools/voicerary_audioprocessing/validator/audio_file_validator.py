import os
import re
import subprocess
import tempfile
import shutil

import ffmpeg

from tools.voicerary_audioprocessing.error_messages import ERR_FILE_NOT_EXISTS, ERR_INVALID_AUDIO_FILE, \
    ERR_NO_RMS_VALUE, ERR_SHORT_DURATION, ERR_LONG_DURATION, ERR_LOW_LOUDNESS_LEVEL, ERR_NO_AUDIO_STREAM, \
    ERR_INVALID_FILE_FOR_PROCESSING, USER_FRIENDLY_ERR_MESSAGES, INTERNAL_ERR_MESSAGES, \
    ERR_INVALID_FILE_PITCH
from tools.voicerary_audioprocessing.utils import AudioProcessingUtils
from tools.voicerary_audioprocessing.voicerary_exception import VoiceraryException


class AudioFileValidator:
    MIN_VALID_LOUDNESS = -40  # in dB
    MIN_VALID_DURATION = 1  # in seconds
    MAX_VALID_DURATION = 1800  # in seconds

    @staticmethod
    def validate(file_path: str, is_music_mode: bool, model_f0max: float) -> bool:
        """

        :param model_f0max:
        :param is_music_mode:
        :param file_path: path to the audio file
        :return: bool if file is valid for further processing
        :raises:
                `FileNotFoundError`
                `ffmpeg.Error`
                `ValueError`
        """
        if not os.path.isfile(file_path):
            raise VoiceraryException(ERR_FILE_NOT_EXISTS.format(file_path=file_path),
                                     USER_FRIENDLY_ERR_MESSAGES[ERR_FILE_NOT_EXISTS])

        ffprobe_output = AudioFileValidator._ffprobe(file_path)
        if AudioFileValidator._has_audio(ffprobe_output) \
                and AudioFileValidator._has_right_duration(ffprobe_output, file_path) \
                and AudioFileValidator._is_loud_enough(file_path) \
                and AudioFileValidator._has_suitable_pitch(file_path, is_music_mode, model_f0max):
            return True

        raise VoiceraryException(ERR_INVALID_FILE_FOR_PROCESSING,
                                 USER_FRIENDLY_ERR_MESSAGES[ERR_INVALID_FILE_FOR_PROCESSING])

    @staticmethod
    def check_duration(file_path: str) -> bool:
        ffprobe_output = AudioFileValidator._ffprobe(file_path)
        return AudioFileValidator._has_right_duration(ffprobe_output, file_path)

    @staticmethod
    def _ffprobe(file_path: str) -> dict:
        try:
            return ffmpeg.probe(file_path)
        except ffmpeg.Error as e:
            raise VoiceraryException(
                INTERNAL_ERR_MESSAGES[ERR_INVALID_AUDIO_FILE].format(file_path=file_path, ffmpeg_err=e.stderr.decode()),
                USER_FRIENDLY_ERR_MESSAGES[ERR_INVALID_AUDIO_FILE])

    @staticmethod
    def _has_audio(ffprobe_output: dict) -> bool:
        if 'streams' not in ffprobe_output or not any(
                stream['codec_type'] == 'audio' for stream in ffprobe_output['streams']):
            raise VoiceraryException(INTERNAL_ERR_MESSAGES[ERR_NO_AUDIO_STREAM],
                                     USER_FRIENDLY_ERR_MESSAGES[ERR_NO_AUDIO_STREAM])

        return True

    @staticmethod
    def _is_loud_enough(file_path: str) -> bool:
        rms = AudioFileValidator._rms_level(file_path)
        if not rms > AudioFileValidator.MIN_VALID_LOUDNESS:
            lufs = AudioFileValidator._lufs_level(file_path)
            if not lufs > AudioFileValidator.MIN_VALID_LOUDNESS:
                raise VoiceraryException(INTERNAL_ERR_MESSAGES[ERR_LOW_LOUDNESS_LEVEL].format(rms=rms, lufs=lufs),
                                         USER_FRIENDLY_ERR_MESSAGES[ERR_LOW_LOUDNESS_LEVEL]
                                         .format(min_rms=AudioFileValidator.MIN_VALID_LOUDNESS))

        return True

    @staticmethod
    def _has_right_duration(ffprobe_output: dict, file_path: str):
        duration = float(ffprobe_output['format']['duration']) if 'duration' in ffprobe_output['format'] else None
        if not duration:
            # force convert to wav if duration was not detected in ffprobe output
            _, tmp_wav_file = tempfile.mkstemp(suffix='.wav')
            (ffmpeg.input(file_path).output(tmp_wav_file)
             .run(overwrite_output=True, capture_stdout=True, capture_stderr=True))
            shutil.copy(tmp_wav_file, file_path)
            os.remove(tmp_wav_file)
            ffprobe_output = AudioFileValidator._ffprobe(file_path)
            duration = float(ffprobe_output['format']['duration'])

        if duration < AudioFileValidator.MIN_VALID_DURATION:
            raise VoiceraryException(INTERNAL_ERR_MESSAGES[ERR_SHORT_DURATION].format(duration=round(duration, 3)),
                                     USER_FRIENDLY_ERR_MESSAGES[ERR_SHORT_DURATION]
                                     .format(min_duration=AudioFileValidator.MIN_VALID_DURATION))

        if duration > AudioFileValidator.MAX_VALID_DURATION:
            max_duration = AudioFileValidator.MAX_VALID_DURATION // 60
            raise VoiceraryException(INTERNAL_ERR_MESSAGES[ERR_LONG_DURATION].format(duration=round(duration)),
                                     USER_FRIENDLY_ERR_MESSAGES[ERR_LONG_DURATION]
                                     .format(max_duration=max_duration))

        return True

    @staticmethod
    def _has_suitable_pitch(file_path: str, is_music_mode: bool, model_f0max: float) -> bool:
        if is_music_mode:
            _, tmp_wav_file = tempfile.mkstemp(suffix='.wav')
            (ffmpeg.input(file_path).output(tmp_wav_file)
             .run(overwrite_output=True, capture_stdout=True, capture_stderr=True))
            input_f0max = AudioProcessingUtils.get_highest_frequency(tmp_wav_file)
            if os.path.isfile(tmp_wav_file):
                os.remove(tmp_wav_file)
            if input_f0max > 0 and input_f0max > model_f0max:
                raise VoiceraryException(INTERNAL_ERR_MESSAGES[ERR_INVALID_FILE_PITCH]
                                         .format(file_f0max=input_f0max, model_f0max=model_f0max),
                                         USER_FRIENDLY_ERR_MESSAGES[ERR_INVALID_FILE_PITCH])

        return True

    @staticmethod
    def _rms_level(file_path: str) -> float:
        command = [
            'ffmpeg',
            '-i', file_path,
            '-filter:a', 'volumedetect',
            '-f', 'null', '/dev/null']

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if result.returncode != 0:
            raise VoiceraryException(
                INTERNAL_ERR_MESSAGES[ERR_NO_RMS_VALUE].format(file_path=file_path, stdout_err=result.stdout.decode()),
                USER_FRIENDLY_ERR_MESSAGES[ERR_NO_RMS_VALUE])

        rms_line = [line for line in result.stdout.decode().split('\n') if 'mean_volume' in line]
        if rms_line:
            rms_level = re.findall(r'mean_volume:\s(-?\d+\.?\d*)\sdB$', rms_line[0])
            return float(rms_level[0])

        return -100.0

    @staticmethod
    def _lufs_level(file_path: str) -> float:
        command = [
            'ffmpeg',
            '-i', file_path,
            '-af', 'ebur128',
            '-f', 'null', '/dev/null']

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if result.returncode != 0:
            raise VoiceraryException(
                INTERNAL_ERR_MESSAGES[ERR_NO_RMS_VALUE].format(file_path=file_path, stdout_err=result.stdout.decode()),
                USER_FRIENDLY_ERR_MESSAGES[ERR_NO_RMS_VALUE])

        lufs_line = None
        output_list = result.stdout.decode().split('\n')
        for i in range(len(output_list)):
            if "Integrated loudness:" in output_list[i] and (i + 1) < len(output_list):
                lufs_line = output_list[i + 1]
                break

        if lufs_line:
            print(lufs_line)
            lufs_level = re.findall(r'I:\s+(-?\d+\.?\d*)\sLUFS$', lufs_line)
            return float(lufs_level[0])

        return -100.0
