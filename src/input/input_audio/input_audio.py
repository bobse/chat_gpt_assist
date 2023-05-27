from typing import Type
from input.input_audio.wakeword.hotword_interface import HotwordInterface
from input.input_audio.listener.listener_interface import ListenerInterface
from input.input_audio.transcriber.transcriber_interface import TranscriberInterface
from input.input_interface import InputInterface
from config.config import logger


class InputAudio(InputInterface):
    def __init__(
        self,
        listener: Type[ListenerInterface],
        transcriber: Type[TranscriberInterface],
        hotword_detector: HotwordInterface = None,
    ) -> None:
        self.listener = listener
        self.transcriber = transcriber
        self.hotword_detector = hotword_detector

    def get_input(self) -> str:
        filename = self.listener.listen()
        logger.debug(f"Audio file saved as: {filename}")
        return self.transcriber.transcribe(filename)
