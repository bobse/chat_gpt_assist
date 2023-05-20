from abc import ABC, abstractmethod


class TranscriberInterface(ABC):
    @staticmethod
    @abstractmethod
    def transcribe(audio_filename: str) -> str:
        raise NotImplementedError()
