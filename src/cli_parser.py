import argparse


class CliParser:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            prog="LLM Assistant",
            description="Simple modular assistant",
        )
        self.parser.add_argument(
            "--input",
            dest="input",
            action="store",
            type=str,
            default="audio",
            choices=["audio", "text"],
            help="Set the input. Default: audio",
        )

        self.parser.add_argument(
            "--output",
            dest="output",
            action="store",
            type=str,
            default="audio",
            choices=["audio", "text"],
            help="Set the output. Default: audio",
        )

        self.parser.add_argument(
            "--refresh_examples",
            action=argparse.BooleanOptionalAction,
            dest="refresh_examples",
            help="Resets the examples embeddings DB",
        )

    def args(self):
        return self.parser.parse_args()
