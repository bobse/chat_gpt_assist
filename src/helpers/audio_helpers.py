import wave
import pyaudio


def play_file(filename) -> None:
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
