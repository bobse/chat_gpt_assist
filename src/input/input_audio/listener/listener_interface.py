from abc import ABC, abstractmethod


class ListenerInterface(ABC):
    @staticmethod
    @abstractmethod
    def listen() -> str:
        raise NotImplementedError()
