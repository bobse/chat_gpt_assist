from input.input_interface import InputInterface


class InputText(InputInterface):
    def user_prompt(self) -> str:
        user_prompt = input("What do you want? ")
        return user_prompt
