from abc import ABC, abstractmethod


class TTSInterface(ABC):
    @staticmethod
    @abstractmethod
    def text_to_speech(text: str) -> str:
        raise NotImplementedError()
