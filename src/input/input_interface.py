from abc import ABC, abstractmethod


class InputInterface(ABC):
    @abstractmethod
    def user_prompt(self) -> str:
        raise NotImplementedError()
