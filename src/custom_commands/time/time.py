from datetime import datetime
from base_command.base_command import BaseCommand
from custom_commands.time.response import Response
from output.output_response import OutputResponse


class Time(BaseCommand):
    @classmethod
    def execute(cls, model_response, assistant):
        cls.parse_validate_response(model_response)
        return OutputResponse(
            success=True,
            raw_text=cls._gen_time_response(),
        )

    @staticmethod
    def _gen_time_response() -> str:
        time = datetime.now()
        hour = time.hour
        minutes = time.minute
        if hour < 10:
            hour = str(hour)[1:]
        if minutes < 10:
            minutes = str(minutes)[1:]
        return f"It's {hour} {minutes}"
