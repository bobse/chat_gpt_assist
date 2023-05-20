class ModelError(Exception):
    def __init__(self, message="Error in the model process") -> None:
        super().__init__(message)
