from datetime import datetime, timedelta
from base_command.base_command import BaseCommand
from custom_commands.time.response import Response
from output.output_response import OutputResponse
from config import config


class Time(BaseCommand):
    @classmethod
    def execute(cls, model_response, assistant):
        response: Response = cls.parse_validate_response(model_response)
        return OutputResponse(
            success=True,
            raw_text=cls._gen_time_response(response),
        )

    @staticmethod
    def _gen_time_response(response: Response) -> str:
        if response.entity is not None and response.timezone is not None:
            time = datetime.utcnow() + timedelta(hours=response.timezone)
        else:
            time = datetime.utcnow() + timedelta(hours=config.TIMEZONE)
        hour = time.hour
        minutes = time.minute
        return f"It's {hour}:{minutes}"
