from input.input_interface import InputInterface
from .listener.listener_pyaudio import ListenerPyAudio
from .transcriber.transcriber_openai import OpenAiTranscriber
from config.config import logger
from config.config import TEMP_AUDIO_FILE


class InputAudio(InputInterface):
    def get_input(self) -> str:
        logger.info("Press any key to record your command")
        input()
        filename = ListenerPyAudio.listen()
        logger.debug(f"Audio file saved as: {filename}")
        return OpenAiTranscriber.transcribe(filename)
