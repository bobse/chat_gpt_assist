import os
from dotenv import load_dotenv
import logging
from pathlib import Path

from config.logger_format import CustomLogFormatter

_ = load_dotenv()

BASE_PATH = Path(".").parent.absolute()

CUSTOM_CMD_FOLDER = os.getenv("CUSTOM_CMD_FOLDER", "custom_commands")
CUSTOM_CMD_FOLDER_PATH = Path(BASE_PATH, "src", CUSTOM_CMD_FOLDER)

EMBEDDINGS_DB = Path(BASE_PATH, "db", ".lancedb")

TEMP_AUDIO_FOLDER = Path(BASE_PATH, "temp/audios")
TEMP_AUDIO_FILE = Path(TEMP_AUDIO_FOLDER, "temp.wav")

ERROR_SOUND = str(Path(BASE_PATH, "assets", "audio", "dong.wav"))
SUCCESS_SOUND = str(Path(BASE_PATH, "assets", "audio", "ding.wav"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("You must specify an OpenAI API key")

PORCUPINE_KEY = os.getenv("PORCUPINE_KEY")

# Language for whisper model
LANGUAGE = os.getenv("LANGUAGE", "en")

logger = logging.getLogger("main_logger")
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
# handler = logging.FileHandler('info.log')
handler = logging.StreamHandler()
handler.setFormatter(CustomLogFormatter())
logger.addHandler(handler)
