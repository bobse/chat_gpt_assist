from typing import Type
from input.input_audio.listener.listener_interface import ListenerInterface
from input.input_audio.transcriber.transcriber_interface import TranscriberInterface
from input.input_interface import InputInterface
from config.config import logger


class InputAudio(InputInterface):
    def __init__(
        self, listener: Type[ListenerInterface], transcriber: Type[TranscriberInterface]
    ) -> None:
        self.listener = listener
        self.transcriber = transcriber

    def get_input(self) -> str:
        logger.info("Press any key to record your command or Ctrl-C to exit")
        input()
        filename = self.listener.listen()
        logger.debug(f"Audio file saved as: {filename}")
        return self.transcriber.transcribe(filename)
