from base_command.base_command import BaseCommand
from custom_commands.ask_gpt.response import Response
from output.output_response import OutputResponse
from prompt.prompt import Prompt
from config import config
import json


class AskGpt(BaseCommand):
    @classmethod
    def execute(cls, model_response, assistant):
        validated_response: Response = cls.parse_validate_response(model_response)
        prompt = Prompt(
            'Answer the question separated by || in no more than 1 paragraph. Try to be as brief as you can. ||{query}||. The answer must be in a json format following this structure: {"answer":"text from the answer here"}',
        )
        answer = assistant.model.process(prompt.generate(validated_response.question))
        config.logger.debug(answer)

        return OutputResponse(
            success=True,
            raw_text=json.loads(answer).get("answer"),
        )
