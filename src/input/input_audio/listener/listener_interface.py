from abc import ABC, abstractmethod


class ListenerInterface(ABC):
    @staticmethod
    @abstractmethod
    def listen(filename: str) -> str:
        raise NotImplementedError()
