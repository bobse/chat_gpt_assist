from abc import ABC, abstractmethod


class InputInterface(ABC):
    @abstractmethod
    def get_input(self) -> str:
        raise NotImplementedError()
