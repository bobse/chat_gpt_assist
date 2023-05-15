from abc import ABC, abstractmethod
from prompter.prompter_response import PrompterResponse
from prompter.example import Example
import json
import os
import inspect
from config import config


class BaseCommand(ABC):
    @classmethod
    def examples(cls) -> list[Example]:
        examples = []
        filename = f"{os.path.dirname(inspect.getfile(cls))}/examples.json"
        try:
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    for example_dict in json.load(file):
                        examples.append(Example(example_dict))
        except Exception as e:
            config.logger.error(e)

        return examples

    @classmethod
    def command_name(cls) -> str:
        return cls.__module__.replace(".py", "")

    @staticmethod
    @abstractmethod
    def execute(response: PrompterResponse) -> str | None:
        raise NotImplementedError()
