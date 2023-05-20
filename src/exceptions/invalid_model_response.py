class InvalidModelResponse(Exception):
    def __init__(self, message="Invalid Model Response") -> None:
        super().__init__(message)
