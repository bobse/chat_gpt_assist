from config import config
from autoloader import AutoLoader
from input.input_text.input_text import InputText
from output.output_text.output_text import OutputText
from prompter.prompter import Prompter


if __name__ == "__main__":
    input = InputText()
    output = OutputText()
    commands = AutoLoader.load_commands()
    config.logger.debug(f"Available commands: {list(commands.keys())}")
    prompter = Prompter(commands)

    while True:
        response = prompter.process_command(input.user_prompt())

        if response:
            if commands.get(response.command):
                output.respond_to_user(commands[response.command].execute(response))
            else:
                config.logger.debug("Invalid command!")
                config.logger.debug(response.command)
        else:
            config.logger.debug("Could not get an answer right now")
