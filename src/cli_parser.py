import argparse


class CliParser:
    _args: argparse.Namespace = None

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(
            prog="LLM Assistant",
            description="Simple modular assistant",
        )
        parser.add_argument(
            "--input",
            dest="input",
            action="store",
            type=str,
            default="audio",
            choices=["audio", "text"],
            help="Set the input. Default: audio",
        )

        parser.add_argument(
            "--output",
            dest="output",
            action="store",
            type=str,
            default="audio",
            choices=["audio", "text"],
            help="Set the output. Default: audio",
        )

        parser.add_argument(
            "--refresh_examples",
            action=argparse.BooleanOptionalAction,
            dest="refresh_examples",
            help="Resets the examples embeddings DB",
        )

        self._args = parser.parse_args()

    def get_input(self) -> str:
        return self._args.input

    def get_output(self) -> str:
        return self._args.output

    def should_reset_db(self) -> bool:
        return self._args.refresh_examples is not None
