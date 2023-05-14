import os
from autoloader import AutoLoader
from input.input_text.input_text import InputText
from output.output_text.output_text import OutputText
from prompter.prompter import Prompter
from dotenv import load_dotenv
import logging

_ = load_dotenv()

logger = logging.getLogger("main_logger")
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
# handler = logging.FileHandler('info.log')
handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


if __name__ == "__main__":
    input = InputText()
    output = OutputText()
    commands = AutoLoader.load_commands()
    logger.debug(f"Available commands: {list(commands.keys())}")
    prompter = Prompter(commands)

    while True:
        response = prompter.process_command(input.user_prompt())

        if response:
            if commands.get(response.command):
                output.respond_to_user(commands[response.command].execute(response))
            else:
                logger.debug("Invalid command!")
                logger.debug(response.command)
        else:
            logger.debug("Could not get an answer right now")
