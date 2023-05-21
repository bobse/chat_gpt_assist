from base_command.base_command import BaseCommand
from custom_commands.lights.response import Response


class Lights(BaseCommand):
    @classmethod
    def execute(cls, model_response, input, model):
        validated_response: Response = cls.parse_validate_response(model_response)
        return f"executing Lights command: {validated_response.action} on {validated_response.entity}"
