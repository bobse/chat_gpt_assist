from collections import deque
from input.input_audio.listener.listener_interface import ListenerInterface
import pyaudio
import wave
from config import config
import numpy as np

FRAMERATE = 44100
TIMEOUT = 8  # Maximum recording duration in seconds
CHUNK = 1024
CHUNK_PER_SEC = FRAMERATE // CHUNK
THRESHOLD = 300  # The threshold intensity that defines silence signal (lower than).
SILENCE_LIMIT = 2


class ListenerPyAudio(ListenerInterface):
    @staticmethod
    def listen(filename: str = config.TEMP_AUDIO_FILE) -> str:
        ListenerPyAudio._save_audio(filename, ListenerPyAudio._record_audio())
        return filename

    @staticmethod
    def _record_audio() -> list[bytes]:
        # Set up the audio stream
        p = pyaudio.PyAudio()
        # Initialize variables
        frames: list[bytes] = []

        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=FRAMERATE,
            input=True,
            frames_per_buffer=CHUNK,
        )
        silence_buffer = deque(maxlen=SILENCE_LIMIT * CHUNK_PER_SEC)

        config.logger.info("Recording...")
        while True:
            data = stream.read(CHUNK)
            frames.append(data)
            silence_buffer.append(np.max(np.frombuffer(data, dtype=np.int16)))

            if len(frames) / CHUNK_PER_SEC > TIMEOUT:
                config.logger.info("Timeout reached. Stopping recording.")
                break

            if len(silence_buffer) == SILENCE_LIMIT * CHUNK_PER_SEC and all(
                [s < THRESHOLD for s in silence_buffer]
            ):
                config.logger.info("Silence detected. Stopping recording.")
                break

            if len(frames) % CHUNK_PER_SEC == 0:
                config.logger.info(".")

        stream.stop_stream()
        stream.close()
        p.terminate()
        return frames

    @staticmethod
    def _save_audio(filename: str, audio_bytes: list[bytes]) -> None:
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
            wf.setframerate(FRAMERATE)
            wf.writeframes(b"".join(audio_bytes))
