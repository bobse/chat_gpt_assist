from abc import ABC, abstractmethod
from response import Response
from example import Example
import json
import os

class BaseCommand(ABC):
	@staticmethod
	def examples():
		examples = []

		with open(f"{os.path.dirname(__file__)}/examples.json", 'r') as file:
			for example_dict in json.load(file):
				examples.append(Example(example_dict))
		return examples

	@classmethod
	def command_name(cls) -> str:
		return cls.__module__.split('.')[-1]

	@staticmethod
	@abstractmethod
	def execute(response: Response):
		raise NotImplementedError()



