from pathlib import Path
import shutil
from cli_parser import CliParser
from config import config

from embeddings.embeddings_local import EmbeddingsLocal
from input.input_audio.listener.listener_pyaudio import ListenerPyAudio
from input.input_audio.transcriber.transcriber_faster_whisper import (
    TranscriberFasterWhisper,
)
from input.input_audio.wakeword.hotword_porcupine import HotwordPorcupine
from input.input_text.input_text import InputText
from input.input_audio.input_audio import InputAudio
from output.output_audio.output_audio import OutputAudio
from output.output_audio.tts.tts_google import TTSGoogle
from output.output_audio.tts.tts_openai import TTSOpenAi
from output.output_text.output_text import OutputText
from assistant.assistant import Assistant
from model.openai.model import OpenAiModel

INPUTS = {
    "text": InputText(),
    "audio": InputAudio(
        ListenerPyAudio, TranscriberFasterWhisper(), HotwordPorcupine()
    ),
}
OUTPUTS = {"text": OutputText(), "audio": OutputAudio(TTSOpenAi())}


def reset_db():
    shutil.rmtree(Path(config.EMBEDDINGS_DB, "commands.lance"))


if __name__ == "__main__":
    cliParser = CliParser()
    config.logger.info("Starting assistant...")
    if cliParser.should_reset_db():
        config.logger.info("Refreshing Examples Database")
        reset_db()

    assistant = Assistant(
        INPUTS[cliParser.get_input()],
        OUTPUTS[cliParser.get_output()],
        OpenAiModel,
        EmbeddingsLocal("commands"),
    )
    assistant.loop()
