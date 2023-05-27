import json
import os
from pathlib import Path
from config import config

EX_TEMPLATE = [
    {
        "user_input": "",
        "action": "",
        "entity": "",
    }
]

REPONSE_CONTENT = """from pydantic import BaseModel


class Response(BaseModel):
    user_input: str
    action: str
    entity: str
"""

COMMAND_CONTENT = """from base_command.base_command import BaseCommand
from custom_commands.{{cmd_name}}.response import Response


class {{command}}(BaseCommand):
    @classmethod
    def execute(cls, assistant):
        validated_response: Response = cls.parse_validate_response(model_response)
        return f"executing {{command}} command: {validated_response.action} on {validated_response.entity}"
"""


def _get_file_fullpath(filename, cmd_path) -> str:
    return Path(cmd_path, filename)


def _camel_case(name: str) -> str:
    return "".join([w[0].upper() + w[1:] for w in name.lower().split("_")])


def _generate_cmd_file(cmd_name: str) -> str:
    return COMMAND_CONTENT.replace("{{cmd_name}}", cmd_name).replace(
        "{{command}}", _camel_case(cmd_name)
    )


def create_new_command(cmd_name: str) -> None:
    if cmd_name.lower() != cmd_name:
        raise ValueError("Commands must be in snake_case format.")

    cmd_path = Path(config.CUSTOM_CMD_FOLDER_PATH, cmd_name).resolve()

    if os.path.exists(cmd_path):
        raise FileExistsError(f"You already have a command with that name {cmd_name}")

    os.mkdir(cmd_path)

    with open(_get_file_fullpath("examples.json", cmd_path), "w") as example_file:
        example_file.write(json.dumps(EX_TEMPLATE, indent=4))

    with open(_get_file_fullpath("response.py", cmd_path), "w") as response_file:
        response_file.write(REPONSE_CONTENT)

    with open(_get_file_fullpath(f"{cmd_name}.py", cmd_path), "w") as cmd_file:
        cmd_file.write(_generate_cmd_file(cmd_name))


if __name__ == "__main__":
    cmd_name = input("What would the new command name be? ")
    print(f"Generating new command in: {Path(config.CUSTOM_CMD_FOLDER_PATH, cmd_name)}")
    create_new_command(cmd_name)
    print("Done!")
