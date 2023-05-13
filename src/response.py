class Response:
    def __init__(self, response: dict):
        self.command = response.get('command')
        self.keywords = response.get('keywords')

