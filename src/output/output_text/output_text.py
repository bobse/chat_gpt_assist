from output.output_interface import OutputInterface


class OutputText(OutputInterface):
    def respond_to_user(self, text_response: str) -> None:
        print(text_response)
