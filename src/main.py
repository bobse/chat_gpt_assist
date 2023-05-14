from autoloader import AutoLoader
from prompter.prompter import Prompter
from dotenv import load_dotenv
import logging

logger = logging.getLogger("main_logger")
logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler('info.log')
handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

_ = load_dotenv()


if __name__ == "__main__":
    commands = AutoLoader.load_commands()
    logger.debug(f"Available commands: {list(commands.keys())}")
    prompter = Prompter(commands)
    while True:
        prompt: Prompter = input("What do you want? ")
        response = prompter.process_command(prompt)

        if response:
            if commands.get(response.command):
                commands[response.command].execute(response)
            else:
                logger.debug("Invalid command!")
                logger.debug(response.command)
        else:
            logger.debug("Could not get an answer right now")
