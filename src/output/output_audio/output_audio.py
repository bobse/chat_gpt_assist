import wave

import pyaudio
from helpers.audio_helpers import play_file
from output.output_audio.tts.tts_interface import TTSInterface
from output.output_interface import OutputInterface
from config import config


class OutputAudio(OutputInterface):
    def __init__(self, tts_module: TTSInterface) -> None:
        self.tts_module = tts_module

    def execute(self, response) -> None:
        if not response.success:
            self.fail()
            return

        if response.raw_text is None or len(response.raw_text) == 0:
            self._play_file(config.SUCCESS_SOUND)
            return

        audio_file = self.tts_module.text_to_speech(response.raw_text)
        self._play_file(audio_file)

    def fail(self):
        self._play_file(config.ERROR_SOUND)

    def _play_file(self, filename) -> None:
        play_file(filename)
