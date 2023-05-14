from base_command.base_command import BaseCommand
from prompter.prompter_response import PrompterResponse


class Lights(BaseCommand):
    @staticmethod
    def execute(response: PrompterResponse):
        print(
            f"executing Lights command: {response.command} | keywords {response.keywords}"
        )
