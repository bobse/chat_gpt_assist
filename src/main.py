import argparse
from config import config
from input.input_audio.listener.listener_pyaudio import ListenerPyAudio
from input.input_audio.transcriber.transcriber_openai import TranscriberOpenAi
from input.input_audio.wakeword.hotword_porcupine import HotwordPorcupine
from input.input_text.input_text import InputText
from input.input_audio.input_audio import InputAudio
from output.output_text.output_text import OutputText
from assistant.assistant import Assistant
from model.openai.model import OpenAiModel

INPUTS = {
    "text": InputText(),
    "audio": InputAudio(ListenerPyAudio, TranscriberOpenAi, HotwordPorcupine()),
}
OUTPUTS = {"text": OutputText()}

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
    default="text",
    choices=["text"],
    help="Set the output. Default: text",
)

if __name__ == "__main__":
    args = parser.parse_args()
    config.logger.info("Starting assistant...")
    assistant = Assistant(INPUTS[args.input], OUTPUTS[args.output], OpenAiModel)
    assistant.loop()
