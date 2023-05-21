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
        self.prompt = self.generate_prompt()
        config.logger.debug("Example Prompt:")
        config.logger.debug(self.prompt.generate("example prompt"))

    def loop(self) -> None:
        while True:
            try:
                user_query = self.input.get_input()

                if user_query.lower() == "quit":
                    config.logger.info("Exiting assistant...")
                    break
                config.logger.info(f"Input: {user_query}")
                model_response = self.model.process(self.prompt.generate(user_query))
                json_response = json.loads(model_response)
                command_key = json_response.get("command")
                if not command_key:
                    raise ModelResponseWithoutCommand()

                if not self.commands.get(command_key):
                    raise UnknownCommand(command_key)

                config.logger.debug(json_response)

                execution_response = self.commands[command_key].execute(
                    json_response, self.input, self.model
                )

                self.output.execute(execution_response)

            # TODO: If necessary, maybe add retry here with reinforcing adding the response into the prompt
            except KeyboardInterrupt:
                config.logger.info("Exiting...")
                break

            except json.JSONDecodeError:
                config.logger.error("Invalid Json response from model")
                config.logger.error(f"Model responded with: {model_response}")

            except (ModelResponseWithoutCommand, UnknownCommand):
                self.output.execute("I can't find this command. Please try again.")

            except InvalidModelResponse as e:
                config.logger.error(e)
                config.logger.error(f"Model responded with: {model_response}")

            except Exception as e:
                config.logger.error("Unknown error:")
                config.logger.error(traceback.format_exc(e))

    def generate_prompt(self) -> Prompt:
        input_variables = {
            "examples": self.get_examples(),
            "commands": ", ".join(self.commands.keys()),
        }
        return Prompt(self.get_base_prompt_text(), input_variables)

    # TODO: Create embeddings for the examples and load them accordinly to user input
    def get_examples(self) -> list[str]:
        examples = []
        for cmd in self.commands.values():
            for ex in cmd.examples():
                examples.append(
                    f"Example {len(examples)+1}: {json.dumps(ex, indent=4)}"
                )
        return examples

    def get_base_prompt_text(self) -> str:
        prompt = "Your job is to classify the text separated by ||."
        prompt += "Here are some of examples of expected responses:\n {examples}"
        prompt += "\n\nYour response must always be in json format in snake case typing and must"
        prompt += "always contain the following keys 'command', 'keywords'."
        prompt += "if you can not classify the command or the keywords,"
        prompt += "the value must be 'unknown'.\n"
        prompt += "Here's  a list of allowed commands: {commands} \n"
        prompt += "\nANSWERS CAN ONLY BE IN JSON FORMAT.  || {query} ||"
        return prompt
