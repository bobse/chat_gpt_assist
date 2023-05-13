import json
import openai
import logging
import os
from response import Response

logger = logging.getLogger('main_logger')


class Prompter:
    def __init__(self, commands: dict):
        self.commands = commands
        self.base_prompt = self._generate_base_prompt()

    def process_command(self, user_prompt: str, model = "gpt-3.5-turbo"):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        logger.info(f"Prompt: {user_prompt}")

        messages = [{"role": "user", "content": self._generate_prompt(user_prompt)}]
        response = openai.ChatCompletion.create(
                model = model,
                messages = messages,
                temperature = 0,
        )
        try:
            return Response(json.loads(response.choices[0].message["content"]))
        except Exception as e:
            logger.error(e._message)


    def _generate_prompt(self, user_prompt):
        return self.base_prompt.replace('#PROMPT_PLACEHOLDER#', user_prompt)

    def _generate_base_prompt(self):
        prompt = "Your job is to classify the text separated by ||. Here are some of examples of expected responses:\n"
        example_number = 1
        for cmd in self.commands.values():
            for ex in cmd.examples():
                prompt += f"Example {example_number}:\n"
                prompt += f"- Text Input: {ex.input}\n"
                prompt += f"- Expected Response in JSON:\n"
                prompt += json.dumps(ex.response, indent = 2)
                example_number += 1

        prompt += "\n\nYour response must always be in json format in snake case typing and must always contain the"
        prompt += """following keys "command", "keywords". if you can not classify """
        prompt += """the command or the keywords, the value must be "unknown".\nHere's  a list of allowed commands:\n"""
        prompt += ', '.join(self.commands.keys())
        prompt += f"""\nANSWERS CAN ONLY BE IN JSON FORMAT.  || #PROMPT_PLACEHOLDER# ||"""
        return prompt
