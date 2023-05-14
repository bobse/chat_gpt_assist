from base_command.base_command import BaseCommand


class Lights(BaseCommand):
    @staticmethod
    def execute(response):
        return f"executing Lights command: {response.command} | keywords {response.keywords}"
