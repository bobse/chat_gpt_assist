from base_command.base_command import BaseCommand
from custom_commands.ask_gpt.response import Response
from output.output_response import OutputResponse
from prompt.prompt import Prompt


class AskGpt(BaseCommand):
    @classmethod
    def execute(cls, model_response, assistant):
        validated_response: Response = cls.parse_validate_response(model_response)
        prompt = Prompt(
            "Answer the question separated by || in no more than 1 paragraph. Try to be as brief as you can. ||{query}||",
        )
        answer = assistant.model.process(prompt.generate(validated_response.question))
        return OutputResponse(
            success=True,
            raw_text=answer,
        )
