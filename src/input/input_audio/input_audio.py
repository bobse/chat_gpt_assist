from input.input_interface import InputInterface


class InputAudio(InputInterface):
    def user_prompt(self) -> str:
        raise NotImplementedError()
