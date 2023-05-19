from base_command.base_command import BaseCommand


class Lights(BaseCommand):
    @staticmethod
    def execute(model_response):
        validated_response = BaseCommand.parse_validate_response(model_response)
        return f"executing Lights command: {validated_response.action} \
            on {validated_response.entity}"
