import wave
import pyaudio
from pydub import AudioSegment


def play_file(filename) -> None:
    if is_mp3(filename):
        play_mp3(filename)
    else:
        play_wav(filename)


def play_wav(filename) -> None:
    chunk = 1024
    wf = wave.open(filename, "rb")
    py_audio = pyaudio.PyAudio()

    stream = py_audio.open(
        format=py_audio.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True,
    )

    data = wf.readframes(chunk)
    while data != b"":
        stream.write(data)
        data = wf.readframes(chunk)

    stream.close()
    py_audio.terminate()


def play_mp3(filename) -> None:
    sound = AudioSegment.from_mp3(filename)
    sound = sound.set_channels(1)
    audio_data = sound.raw_data

    p = pyaudio.PyAudio()

    try:
        stream = p.open(
            format=p.get_format_from_width(sound.sample_width),
            channels=sound.channels,
            rate=sound.frame_rate,
            output=True,
        )

        stream.write(audio_data)

    finally:
        stream.close()
        p.terminate()


def is_mp3(filename) -> bool:
    return filename[-3:].lower() == "mp3"
