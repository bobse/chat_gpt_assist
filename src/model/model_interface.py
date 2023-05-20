from abc import ABC, abstractmethod


class ModelInterface(ABC):
    @staticmethod
    @abstractmethod
    def process(model_prompt: str) -> str:
        raise NotImplementedError()
