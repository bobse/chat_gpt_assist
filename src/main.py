import argparse
from pathlib import Path
import shutil
from config import config
from embeddings.embeddings_local import EmbeddingsLocal
from input.input_audio.listener.listener_pyaudio import ListenerPyAudio
from input.input_audio.transcriber.transcriber_openai import TranscriberOpenAi
from input.input_audio.wakeword.hotword_porcupine import HotwordPorcupine
from input.input_text.input_text import InputText
from input.input_audio.input_audio import InputAudio
from output.output_audio.output_audio import OutputAudio
from output.output_audio.tts.tts_google import TTSGoogle
from output.output_text.output_text import OutputText
from assistant.assistant import Assistant
from model.openai.model import OpenAiModel

INPUTS = {
    "text": InputText(),
    "audio": InputAudio(ListenerPyAudio, TranscriberOpenAi, HotwordPorcupine()),
}
OUTPUTS = {"text": OutputText(), "audio": OutputAudio(TTSGoogle)}

parser = argparse.ArgumentParser(
    prog="LLM Assistant",
    description="Simple modular assistant",
)
parser.add_argument(
    "--input",
    dest="input",
    action="store",
    type=str,
    default="audio",
    choices=["audio", "text"],
    help="Set the input. Default: audio",
)

parser.add_argument(
    "--output",
    dest="output",
    action="store",
    type=str,
    default="audio",
    choices=["audio", "text"],
    help="Set the output. Default: audio",
)

parser.add_argument(
    "--refresh_examples",
    action=argparse.BooleanOptionalAction,
    dest="refresh_examples",
    help="Resets the examples embeddings DB",
)


def reset_db():
    shutil.rmtree(Path(config.EMBEDDINGS_DB, "commands.lance"))


if __name__ == "__main__":
    args = parser.parse_args()
    config.logger.info("Starting assistant...")
    if args.refresh_examples:
        config.logger.info("Refreshing Examples Database")
        reset_db()

    assistant = Assistant(
        INPUTS[args.input],
        OUTPUTS[args.output],
        OpenAiModel,
        EmbeddingsLocal("commands"),
    )
    assistant.loop()
