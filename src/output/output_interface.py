from abc import ABC, abstractmethod


class OutputInterface(ABC):
    @abstractmethod
    def execute(self, text_response: str):
        raise NotImplementedError()
