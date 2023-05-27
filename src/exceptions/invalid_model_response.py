class InvalidModelResponse(Exception):
    def __init__(self, model_response, message="Invalid Model Response") -> None:
        self.model_response = model_response
        super().__init__(message)
