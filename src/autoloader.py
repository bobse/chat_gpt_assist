import inspect
import os
import importlib

class AutoLoader:
	BASEFOLDER = './custom_commands'

	@classmethod
	def load_commands(cls)-> dict:
		commands = {}
		for cmd in cls.load_files():
			class_ = AutoLoader.load_module(cmd)
			if class_:
				commands[cmd] = class_

		return commands

	@classmethod
	def load_files(cls):
		return [folder for folder in next(os.walk(cls.BASEFOLDER))[1] if folder[0] != '_']

	@staticmethod
	def camel_case_transform(command: str):
		return ''.join([w[0].upper()+w[1:] for w in command.split('_')])

	@classmethod
	def load_module(cls, module_name):
		try:
			module = importlib.import_module(f"custom_commands.{module_name}.{module_name}", None)
			class_ = getattr(module, AutoLoader.camel_case_transform(module_name))

			if inspect.isabstract(class_):
				return None
			return class_
		except Exception as e:
			return None


