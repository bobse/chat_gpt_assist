from typing import TypedDict


class dict_response(TypedDict):
    command: str
    keywords: list[str]
    user_input: str


class PrompterResponse:
    def __init__(self, response: dict_response):
        self.command = response.get("command")
        self.keywords = response.get("keywords")
        self.user_input = response.get("user_input")
