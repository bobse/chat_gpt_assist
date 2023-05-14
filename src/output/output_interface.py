from abc import ABC, abstractmethod


class OutputInterface(ABC):
    @abstractmethod
    def respond_to_user(self, text_response: str):
        raise NotImplementedError()
