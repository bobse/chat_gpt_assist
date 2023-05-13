from custom_commands.base_command.base_command import BaseCommand


class OnOff(BaseCommand):
	@staticmethod
	def execute(response):
		print(f"executing turn ON/OFF command: {response.command} | keywords {response.keywords}")
