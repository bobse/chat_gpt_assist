from input.input_interface import InputInterface


class InputAudio(InputInterface):
    def get_input(self) -> str:
        raise NotImplementedError()
