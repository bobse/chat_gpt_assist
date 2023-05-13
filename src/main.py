from autoloader import AutoLoader
from prompter import Prompter
from pprint import pprint
from dotenv import load_dotenv
import logging
import os

logger = logging.getLogger('main_logger')
logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler('info.log')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s | %(asctime)s | %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

_ = load_dotenv()


if __name__ == '__main__':
	commands = AutoLoader.load_commands()
	prompter = Prompter(commands)
	while True:
		prompt = input('What do you want? ')
		response = prompter.process_command(prompt)

		if commands.get(response.command):
			commands[response.command].execute(response)
		else:
			logger.info('Invalid command!')
			logger.debug(response.command)
