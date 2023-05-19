from base_command.base_command import BaseCommand


class TvControl(BaseCommand):
    @staticmethod
    def execute(model_response: str):
        validated_response = BaseCommand.parse_validate_response(model_response)
        return f"executing tv command: \
            {validated_response.action} > {validated_response.entity}"
