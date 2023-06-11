from abc import ABC, abstractmethod


class TranscriberInterface(ABC):
    @abstractmethod
    def transcribe(self, audio_filename: str) -> str:
        raise NotImplementedError()
