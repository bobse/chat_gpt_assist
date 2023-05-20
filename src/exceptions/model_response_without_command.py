class ModelResponseWithoutCommand(Exception):
    def __init__(
        self, message="Model response Json doesnt contain command key"
    ) -> None:
        super().__init__(message)
