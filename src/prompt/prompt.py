from exceptions.invalid_prompt import InvalidPromptException


class Prompt:
    def __init__(
        self, base_text: str, input_variables: None | dict[str, str | list] = None
    ) -> None:
        self.base_text = base_text
        self.check_query_placeholder()
        self.input_variables = input_variables

    def generate(self, user_query) -> str:
        generated_prompt = self.base_text.replace("{query}", user_query)
        if self.input_variables:
            for key, value in self.input_variables.items():
                if isinstance(value, list):
                    value = "\n ".join(value)

                generated_prompt = generated_prompt.replace("{" + key + "}", value)
        return generated_prompt

    def check_query_placeholder(self) -> None:
        if "{query}" not in self.base_text:
            raise InvalidPromptException(
                "{query} placeholder must be present in the base Prompt"
            )
