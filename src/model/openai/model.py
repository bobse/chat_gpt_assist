from exceptions.model_error import ModelError
from model.model_interface import ModelInterface
from openai import OpenAI
from config import config


client = OpenAI(api_key=config.OPENAI_API_KEY)


class OpenAiModel(ModelInterface):
    @staticmethod
    def process(model_prompt, temperature: int = 0, model="gpt-4-1106-preview"):
        try:
            messages = [{"role": "user", "content": model_prompt}]
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                response_format={"type": "json_object"},
            )
            config.logger.debug(response)

            return response.choices[0].message.content
        except Exception as ex:
            config.logger.error(ex)
            raise ModelError(ex) from ex
