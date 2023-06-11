from output.output_audio.tts.tts_interface import TTSInterface
from google.cloud import texttospeech
from config import config


class TTSGoogle(TTSInterface):
    def __init__(self) -> None:
        self.client = texttospeech.TextToSpeechClient()
        self.voice = texttospeech.VoiceSelectionParams(
            language_code=config.TTS_LANGUAGE,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        )
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16, speaking_rate=1.2
        )

    def text_to_speech(self, text: str) -> str:
        synthesis_input = texttospeech.SynthesisInput(text=text)

        response = self.client.synthesize_speech(
            input=synthesis_input, voice=self.voice, audio_config=self.audio_config
        )
        filename = f"{config.TEMP_AUDIO_FOLDER}/output.wav"
        with open(filename, "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)

        return filename
