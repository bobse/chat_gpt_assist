from base_command.base_command import BaseCommand


class TvControl(BaseCommand):
    @staticmethod
    def execute(response):
        return (
            f"executing tv command: {response.command} | keywords {response.keywords}"
        )
