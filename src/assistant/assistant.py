import json
import traceback
from typing import Type
from autoloader import AutoLoader
from embeddings.embeddings_interface import EmbeddingsInterface
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
        embeddings: EmbeddingsInterface,
    ) -> None:
        self.input = input
        self.output = output
        self.model = model
        self.commands = AutoLoader.load_commands()
        self.embeddings = embeddings
        if self.embeddings.empty():
            self._insert_examples_into_table()

    def loop(self) -> None:
        while True:
            try:
                user_input = self._process_input()
                json_response = self._check_cmd_cache(user_input)

                if json_response is None:
                    config.logger.debug("No command in cache. Starting pipeline...")
                    json_response = self._pipe(
                        user_input,
                        [
                            self._create_prompt_with_examples,
                            self.model.process,
                            self._process_model_response,
                        ],
                    )

                cmd_key = json_response["command"]
                command_response = self.commands[cmd_key].execute(json_response, self)

                self.output.execute(command_response)
                self._cache_model_response(json_response)

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

    def _process_model_response(self, model_response: str) -> dict:
        json_response = json.loads(model_response)
        command_key = json_response.get("command")

        if not command_key:
            raise ModelResponseWithoutCommand()
        if not self.commands.get(command_key):
            raise UnknownCommand(command_key)

        config.logger.debug(json_response)
        return json_response

    def _check_cmd_cache(self, user_input: str) -> None | dict:
        similar_queries = self.embeddings.get_similar(user_input, 1)

        if similar_queries[0]["score"] > 90:
            return None
        return similar_queries[0]["data"]

    def _cache_model_response(self, json_response: dict) -> None:
        self.embeddings.insert_into_db(json_response)

    def _input_to_key_format(self, user_input: str) -> str:
        return user_input.lower().replace(" ", "").replace(".", "")

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

    def _create_prompt_with_examples(self, user_query: str) -> Prompt:
        input_variables = {
            "examples": self._get_examples(user_query),
            "commands": ", ".join(self.commands.keys()),
        }
        full_prompt = Prompt(self._get_base_prompt_text(), input_variables).generate(
            user_query
        )
        config.logger.debug(f"Final Prompt: {full_prompt}")
        return full_prompt

    def _get_examples(self, user_query: str) -> list[str]:
        examples = []
        similar_examples = self.embeddings.get_similar(user_query, 10)

        for ex in similar_examples:
            examples.append(
                f"Example {len(examples)+1}: {json.dumps(ex['data'], indent=4)}"
            )
        return examples

    def _insert_examples_into_table(self) -> None:
        config.logger.debug("Recreating embeddings for commands/examples...")
        for cmd in self.commands.values():
            for ex in cmd.examples():
                self.embeddings.insert_into_db(ex)
