from abc import ABC, abstractmethod


class ModelInterface(ABC):
    @abstractmethod
    @staticmethod
    def process() -> str:
        raise NotImplementedError()
