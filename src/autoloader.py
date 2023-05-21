import inspect
import os
import importlib
from base_command.base_command import BaseCommand
from config import config


class AutoLoader:
    COMMAND_FOLDER = config.CUSTOM_CMD_FOLDER_PATH

    @classmethod
    def load_commands(cls) -> dict[str, BaseCommand]:
        commands = {}
        for cmd in cls.load_files():
            class_ = AutoLoader.load_module(cmd)
            if class_:
                commands[cmd] = class_

        config.logger.debug(f"Available commands: {list(commands.keys())}")
        return commands

    @classmethod
    def load_files(cls) -> list[str]:
        return [
            folder
            for folder in next(os.walk(cls.COMMAND_FOLDER))[1]
            if folder[0] != "_"
        ]

    @staticmethod
    def camel_case_transform(command: str) -> str:
        return "".join([w[0].upper() + w[1:] for w in command.lower().split("_")])

    @classmethod
    def load_module(cls, module_name) -> BaseCommand | None:
        try:
            module = importlib.import_module(
                f"custom_commands.{module_name}.{module_name}", None
            )
            class_ = getattr(module, AutoLoader.camel_case_transform(module_name))

            if inspect.isabstract(class_) or not issubclass(class_, BaseCommand):
                return None
            return class_
        except Exception as e:
            config.logger.error(e)
            return None
