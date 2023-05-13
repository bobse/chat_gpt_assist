from pprint import pprint
from dotenv import load_dotenv, find_dotenv
import logging
import chatgpt

logger = logging.getLogger('main_logger')
logger.setLevel(logging.INFO)
# handler = logging.FileHandler('info.log')
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s | %(asctime)s | %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

_ = load_dotenv(find_dotenv())


while True:
    prompt = input('What do you want?')
    response = chatgpt.process_command(prompt)
    pprint(response)

