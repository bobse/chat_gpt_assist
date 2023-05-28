import json
import traceback
from typing import Type
from autoloader import AutoLoader
from exceptions.unknown_command import UnknownCommand
from exceptions.invalid_model_response import InvalidModelResponse
from exceptions.model_response_without_command import ModelResponseWithoutCommand
from input.input_interface import InputInterface
from model.model_interface import ModelInterface
from output.output_interface import OutputInterface
from config import config
from prompt.prompt import Prompt


class Assistant:
    def __init__(
        self,
        input: InputInterface,
        output: OutputInterface,
        model: Type[ModelInterface],
    ) -> None:
        self.input = input
        self.output = output
        self.model = model
        self.commands = AutoLoader.load_commands()
        self.prompt = self._generate_prompt()
        config.logger.debug("Example Prompt:")
        config.logger.debug(self.prompt.generate("example prompt"))
        self.cmd_cache = {}

    def loop(self) -> None:
        while True:
            try:
                user_input = self._process_input()

                if self._is_response_in_cache(user_input):
                    input_key = self._clean_input(user_input)
                    json_response = self.cmd_cache[input_key]
                    config.logger.debug("Using cached command")
                else:
                    json_response = self._pipe(
                        user_input,
                        [
                            self.prompt.generate,
                            self.model.process,
                            self._process_model_response,
                        ],
                    )

                cmd_key = json_response["command"]
                command_response = self.commands[cmd_key].execute(json_response, self)
                self.output.execute(command_response)

            # TODO: If necessary, maybe add retry here with reinforcing adding the response into the prompt
            except KeyboardInterrupt:
                config.logger.info("Exiting...")
                break

            except json.JSONDecodeError as ex:
                config.logger.error("Invalid Json response from model")
                config.logger.error(f"Model responded with: {ex.doc}")
                self.output.fail()

            except (ModelResponseWithoutCommand, UnknownCommand):
                self.output.fail()

            except InvalidModelResponse as ex:
                config.logger.error(ex)
                config.logger.error(f"Model responded with: {ex.model_response}")
                self.output.fail()

            except Exception as ex:
                config.logger.error("Unknown error:")
                config.logger.error(traceback.format_exc(ex))
                self.output.fail()

    def _pipe(self, initial_value, funcs):
        if initial_value is None:
            value = funcs[0]()
        else:
            value = funcs[0](initial_value)

        for fn in funcs[1:]:
            value = fn(value)
        return value

    def _process_input(self):
        if hasattr(self.input, "hotword_detector"):
            self.input.hotword_detector.loop_until_detection()

        user_query = self.input.get_input()
        config.logger.info(f"Input: {user_query}")

        return user_query

    def _generate_prompt(self) -> Prompt:
        input_variables = {
            "examples": self._get_examples(),
            "commands": ", ".join(self.commands.keys()),
        }
        return Prompt(self._get_base_prompt_text(), input_variables)

    def _process_model_response(self, model_response: str) -> dict:
        json_response = json.loads(model_response)
        command_key = json_response.get("command")

        if not command_key:
            raise ModelResponseWithoutCommand()
        if not self.commands.get(command_key):
            raise UnknownCommand(command_key)

        config.logger.debug(json_response)
        self._cache_model_response(json_response)
        return json_response

    def _is_response_in_cache(self, user_input: str) -> bool:
        key = self._clean_input(user_input)
        return self.cmd_cache.get(key) is not None

    def _cache_model_response(self, json_response: dict) -> None:
        prepared_input = self._clean_input(json_response["user_input"])
        self.cmd_cache[prepared_input] = json_response

    def _clean_input(self, user_input: str) -> str:
        return user_input.lower().replace(" ", "").replace(".", "")

    # TODO: Create embeddings for the examples and load them accordinly to user input
    def _get_examples(self) -> list[str]:
        examples = []
        for cmd in self.commands.values():
            for ex in cmd.examples():
                examples.append(
                    f"Example {len(examples)+1}: {json.dumps(ex, indent=4)}"
                )
        return examples

    def _get_base_prompt_text(self) -> str:
        prompt = "Your job is to classify the text separated by ||."
        prompt += "Here are some of examples of expected responses:\n {examples}"
        prompt += "\n\nYour response must always be in json format in snake case typing and must"
        prompt += "always contain the following keys 'command', 'keywords'."
        prompt += "if you can not classify the command or the keywords,"
        prompt += "the value must be 'unknown'.\n"
        prompt += "Here's  a list of allowed commands: {commands} \n"
        prompt += "\nANSWERS CAN ONLY BE IN JSON FORMAT.  || {query} ||"
        return prompt
