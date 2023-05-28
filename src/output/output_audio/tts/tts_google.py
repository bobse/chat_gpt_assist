from output.output_audio.tts.tts_interface import TTSInterface


class TTSGoogle(TTSInterface):
    @staticmethod
    def text_to_speech(text: str) -> str:
        raise NotImplementedError()
