import json


class Example:
	def __init__(self, example: dict):
		self.input = example['user_input']
		self.response = example['response']

	def __str__(self):
		return json.dumps({"user_input": self.input, "expected_response": self.response}, indent=2)
