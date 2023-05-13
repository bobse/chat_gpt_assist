from abc import ABC, abstractmethod
from response import Response
from example import Example
import json
import os
import inspect

class BaseCommand(ABC):
	@classmethod
	def examples(cls):
		examples = []
		filename = f"{os.path.dirname(inspect.getfile(cls))}/examples.json"
		if os.path.exists(filename):
			with open(filename, 'r') as file:
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



