import json


class Example:
    def __init__(self, example: dict):
        self.input: str = example["user_input"]
        self.keywords: list = example["keywords"]

    def prepare_json(self, class_name: str) -> str:
        return json.dumps(
            {
                "user_input": self.input,
                "keywords": self.keywords,
                "command": class_name,
            },
            indent=2,
        )
