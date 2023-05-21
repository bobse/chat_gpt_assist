import os
from dotenv import load_dotenv
import logging
import pathlib

from config.logger_format import CustomLogFormatter

_ = load_dotenv()

CUSTOM_CMD_FOLDER = os.getenv("CUSTOM_CMD_FOLDER", "custom_commands")
TEMP_AUDIO_FOLDER = pathlib.Path("./temp/audios").resolve()
TEMP_AUDIO_FILE = os.path.join(TEMP_AUDIO_FOLDER, "temp.wav")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("You must specify an OpenAI API key")

logger = logging.getLogger("main_logger")
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
# handler = logging.FileHandler('info.log')
handler = logging.StreamHandler()
handler.setFormatter(CustomLogFormatter())
logger.addHandler(handler)