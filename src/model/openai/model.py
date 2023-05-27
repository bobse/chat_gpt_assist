from exceptions.model_error import ModelError
from model.model_interface import ModelInterface
import openai
from config import config

openai.api_key = config.OPENAI_API_KEY


class OpenAiModel(ModelInterface):
    @staticmethod
    def process(model_prompt, temperature: int = 0, model="gpt-3.5-turbo"):
        try:
            messages = [{"role": "user", "content": model_prompt}]
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
            )
            config.logger.debug(response)
            return response.choices[0].message["content"]
        except Exception as ex:
            config.logger.error(ex)
            raise ModelError(ex) from ex
