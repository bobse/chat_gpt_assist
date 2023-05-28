from base_command.base_command import BaseCommand
from custom_commands.ask_gpt.response import Response
from output.output_response import OutputResponse


class AskGpt(BaseCommand):
    @classmethod
    def execute(cls, model_response, assistant):
        validated_response: Response = cls.parse_validate_response(model_response)
        answer = assistant.model.process(validated_response.question)
        return OutputResponse(
            success=True,
            raw_text=answer,
        )
