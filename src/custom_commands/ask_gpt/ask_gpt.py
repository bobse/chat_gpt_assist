from base_command.base_command import BaseCommand
from custom_commands.ask_gpt.response import Response


class AskGpt(BaseCommand):
    @classmethod
    def execute(cls, model_response, input, model):
        validated_response: Response = cls.parse_validate_response(model_response)
        answer = model.process(validated_response.question)
        return answer
