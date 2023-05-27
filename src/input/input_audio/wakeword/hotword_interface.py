from abc import ABC, abstractmethod


class HotwordInterface(ABC):
    @abstractmethod
    def loop_until_detection(self) -> None:
        raise NotImplementedError()
