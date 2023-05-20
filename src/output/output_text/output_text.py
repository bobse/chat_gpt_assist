from output.output_interface import OutputInterface


class OutputText(OutputInterface):
    def execute(self, text_response: str) -> None:
        print(text_response)
