class Response:
    def __init__(self, response: dict):
        self.command = response.get('command')
        self.full_text = response.get('full_text')
        self.keywords = response.get('keywords')
        self.num_tokens = response.get('num_tokens')

