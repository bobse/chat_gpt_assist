from __future__ import annotations
from abc import ABC, abstractmethod
from pydantic import BaseModel

import importlib
import json
import os
import inspect
from config import config

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from assistant.assistant import Assistant


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
                        validated_example = cls.parse_validate_response(
                            example_dict
                        ).dict()
                        validated_example["command"] = cls.command_name()
                        examples.append(validated_example)
        except Exception as e:
            config.logger.error(f"Error loading example from {cls.command_name()}.py")
            config.logger.error(e)

        return examples

    @classmethod
    def command_name(cls) -> str:
        return cls.__module__.split(".")[-1]

    @classmethod
    @abstractmethod
    def execute(cls, model_response: dict, assistant: Assistant) -> str | None:
        raise NotImplementedError()

    @classmethod
    def parse_validate_response(cls, model_response: dict) -> BaseModel:
        validator_class = cls.__load_validator()

        if type(model_response) is dict:
            try:
                parsed_response = validator_class(**model_response)
            except Exception:
                raise InvalidModelResponse(model_response)
        else:
            raise TypeError("Parameter should be dict")

        return parsed_response

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
