class InvalidPromptException(Exception):
    def __init__(self, message="Invalid Prompt") -> None:
        super().__init__(message)
