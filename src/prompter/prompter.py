import json
import openai
import logging
import os
from base_command.base_command import BaseCommand
from prompter.prompter_response import PrompterResponse

logger = logging.getLogger("main_logger")


class Prompter:
    def __init__(self, commands: dict):
        self.commands = commands
        self.base_prompt = self._generate_base_prompt()

    def process_command(
        self, user_prompt: str, show_prompt=False, model="gpt-3.5-turbo"
    ):
        try:
            openai.api_key = os.getenv("OPENAI_API_KEY")
            logger.debug(f"Prompt: {user_prompt}")
            full_prompt = self._generate_prompt(user_prompt)

            if show_prompt:
                logger.debug(full_prompt)

            messages = [{"role": "user", "content": full_prompt}]
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=0,
            )

            raw_response = json.loads(response.choices[0].message["content"])
            logger.debug(json.dumps(raw_response, indent=2))

            return PrompterResponse(raw_response)

        except Exception as e:
            logger.error(e._message)

    def _generate_prompt(self, user_prompt):
        return self.base_prompt.replace("#PROMPT_PLACEHOLDER#", user_prompt)

    def _generate_base_prompt(self):
        prompt = "Your job is to classify the text separated by ||."
        prompt += "Here are some of examples of expected responses:\n"
        example_number = 1
        cmd: BaseCommand
        for cmd_name, cmd in self.commands.items():
            for ex in cmd.examples():
                prompt += f"\nExample {example_number}:\n"
                prompt += f"- Text Input: {ex.input}\n"
                prompt += "- Expected Response in JSON:\n"
                prompt += ex.prepare_json(cmd_name)
                example_number += 1

        prompt += "\n\nYour response must always be in json format in snake case typing and must always contain the"
        prompt += """following keys "command", "keywords". if you can not classify """
        prompt += """the command or the keywords, the value must be "unknown".\nHere's  a list of allowed commands:\n"""
        prompt += ", ".join(self.commands.keys())
        prompt += "\nANSWERS CAN ONLY BE IN JSON FORMAT.  || #PROMPT_PLACEHOLDER# ||"
        return prompt
