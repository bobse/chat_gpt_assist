# this file has the basic assistant

# 1. autoload commands
# 1.5 generate examples
# 2. creates prompt
# 3.

import json
from input.input_interface import InputInterface
from model.model_interface import ModelInterface
from output.output_interface import OutputInterface


class Assistant:
    def __init__(
        self, input: InputInterface, output: OutputInterface, model: ModelInterface
    ) -> None:
        self.input = input
        self.output = output
        self.model = model
        # create prompt instance here

    def loop(self) -> None:
        user_query = self.input.get_input()
        model_response = self.model.process(self.prompt.generate(user_query))
        # json.loads(model_response)
