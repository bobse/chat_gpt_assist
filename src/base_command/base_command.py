from abc import ABC, abstractmethod
import importlib
import json
import os
import inspect
from config import config
from pydantic import BaseModel, ValidationError


class BaseCommand(ABC):
    @classmethod
    def examples(cls) -> list[dict]:
        examples = []
        filename = f"{os.path.dirname(inspect.getfile(cls))}/examples.json"
        try:
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    for example_dict in json.load(file):
                        validated_example = cls.parse_validate_response(example_dict)
                        validated_example["command"] = cls.command_name()
                        examples.append(validated_example)
        except ValidationError as e:
            config.logger.info(
                f"Mal formatted example: {json.dumps(example_dict, indent=2)}"
            )
            config.logger.info(e)
        except Exception as e:
            config.logger.error(e)

        return examples

    @classmethod
    def command_name(cls) -> str:
        return cls.__module__.replace(".py", "")

    @abstractmethod
    @staticmethod
    def execute(model_response: str) -> str | None:
        raise NotImplementedError()

    @classmethod
    def parse_validate_response(cls, model_response: dict) -> dict:
        validator_class = cls.__load_validator()
        # if type(model_response) is str:
        #     parsed_response = validator_class.parse_raw(model_response)
        if type(model_response) is dict:
            parsed_response = validator_class(model_response)
        else:
            raise TypeError("Parameter should be dict or str")

        return parsed_response.dict()

    @classmethod
    def __load_validator(cls) -> BaseModel:
        module = importlib.import_module(
            f"custom_commands.{cls.command_name}.response", None
        )
        validator_class = getattr(module, "Response")

        if not issubclass(validator_class, BaseModel):
            raise TypeError(
                "Validation file must contain a Response object from Pydantic's BaseModel"
            )
        return validator_class
