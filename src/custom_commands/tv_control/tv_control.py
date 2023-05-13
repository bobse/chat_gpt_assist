from custom_commands.base_command.base_command import BaseCommand


class TvControl(BaseCommand):
	@staticmethod
	def execute(response):
		print(f"executing tv command: {response.command} | keywords {response.keywords}")
