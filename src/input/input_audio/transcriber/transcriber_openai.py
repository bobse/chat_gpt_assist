import openai
from input.input_audio.transcriber.transcriber_interface import TranscriberInterface
from config import config

openai.api_key = config.OPENAI_API_KEY


class OpenAiTranscriber(TranscriberInterface):
    @staticmethod
    def transcribe(audio_filename) -> str:
        audio_file = open(audio_filename, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript["text"]
