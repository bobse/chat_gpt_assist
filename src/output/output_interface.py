from abc import ABC, abstractmethod

from output.output_response import OutputResponse


class OutputInterface(ABC):
    @abstractmethod
    def execute(self, response: OutputResponse):
        if not response.success:
            self.fail()

    @abstractmethod
    def fail(self) -> None:
        raise NotImplementedError()
