from config import config
from input.input_text.input_text import InputText
from input.input_audio.input_audio import InputAudio
from output.output_text.output_text import OutputText
from assistant.assistant import Assistant
from model.openai.model import OpenAiModel

if __name__ == "__main__":
    input = InputAudio()
    output = OutputText()
    config.logger.info("Starting assistant...")
    assistant = Assistant(input, output, OpenAiModel)
    assistant.loop()
