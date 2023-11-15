from pathlib import Path
from faster_whisper import WhisperModel
from input.input_audio.transcriber.transcriber_interface import TranscriberInterface
from config import config


class TranscriberFasterWhisper(TranscriberInterface):
    def __init__(self) -> None:
        self.lang = config.LANGUAGE
        model_size = "base.en"
        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8",
            download_root=Path(config.BASE_PATH, "temp/models"),
            cpu_threads=4,
            local_files_only=False,
        )

    def transcribe(self, audio_filename: str) -> str:
        segments, _ = self.model.transcribe(
            audio_filename,
            language=self.lang,
            beam_size=5,
            initial_prompt="ChatGPT may be in the question.",
        )
        return " ".join([segment.text for segment in segments])
