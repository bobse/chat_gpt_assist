from base_command.base_command import BaseCommand


class TvControl(BaseCommand):
    @classmethod
    def execute(cls, model_response):
        validated_response = cls.parse_validate_response(model_response)
        return f"executing tv command: \
            {validated_response['action']} > {validated_response['entity']}"
