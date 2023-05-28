from output.output_interface import OutputInterface


class OutputText(OutputInterface):
    def execute(self, response) -> None:
        if response.success:
            print(response.raw_text)
        else:
            self.fail()

    def fail(self):
        print("Command failed")
