from abc import ABC, abstractmethod
import importlib
import json
import os
import inspect
from config import config
from pydantic import BaseModel, ValidationError

from exceptions.invalid_model_response import InvalidModelResponse


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
            config.logger.error(
                f"Mal formatted example: {json.dumps(example_dict, indent=2)}"
            )
            config.logger.info(e)
        except Exception as e:
            config.logger.error(f"Error loading example from {cls.command_name()}")
            config.logger.error(e)

        return examples

    @classmethod
    def command_name(cls) -> str:
        return cls.__module__.split(".")[-1]

    @classmethod
    @abstractmethod
    def execute(model_response: dict) -> str | None:
        raise NotImplementedError()

    @classmethod
    def parse_validate_response(cls, model_response: dict) -> dict:
        validator_class = cls.__load_validator()
        # if type(model_response) is str:
        #     parsed_response = validator_class.parse_raw(model_response)
        if type(model_response) is dict:
            try:
                parsed_response = validator_class(**model_response)
            except Exception as e:
                raise InvalidModelResponse(e)
        else:
            raise TypeError("Parameter should be dict")

        return parsed_response.dict()

    @classmethod
    def __load_validator(cls) -> BaseModel:
        # base_module_path = ".".join(cls.command_name().split(".")[:-1])

        module = importlib.import_module(
            f"{config.CUSTOM_CMD_FOLDER}.{cls.command_name()}.response", None
        )
        validator_class = getattr(module, "Response")
        if not issubclass(validator_class, BaseModel):
            raise TypeError(
                "Validation file must contain a Response object from Pydantic's BaseModel"
            )

        return validator_class
