import struct
import pvporcupine
import pyaudio

from config import config

from input.input_audio.wakeword.hotword_interface import HotwordInterface


class HotwordPorcupine(HotwordInterface):
    def __init__(self, keywords: list = None) -> None:
        self.keywords = keywords or ["alexa", "jarvis"]
        self.detector = pvporcupine.create(
            access_key=config.PORCUPINE_KEY, keywords=self.keywords
        )

    def loop_until_detection(self):
        p_audio = pyaudio.PyAudio()

        stream = p_audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.detector.sample_rate,
            input=True,
            frames_per_buffer=self.detector.frame_length,
        )

        config.logger.info("Waiting for keyword detection...")
        while True:
            data = stream.read(self.detector.frame_length)
            data = struct.unpack_from("h" * self.detector.frame_length, data)

            keywords_idx = self.detector.process(data)

            if keywords_idx >= 0:
                config.logger.info(f"Detected keyword: {self.keywords[keywords_idx]}")
                break

        stream.stop_stream()
        stream.close()
        p_audio.terminate()
