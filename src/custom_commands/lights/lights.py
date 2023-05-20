from base_command.base_command import BaseCommand
from config import config


class Lights(BaseCommand):
    @classmethod
    def execute(cls, model_response):
        validated_response = cls.parse_validate_response(model_response)
        return f"executing Lights command: {validated_response['action']} \
            on {validated_response['entity']}"
