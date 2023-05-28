from base_command.base_command import BaseCommand
from custom_commands.tv_control.response import Response
from output.output_response import OutputResponse


class TvControl(BaseCommand):
    @classmethod
    def execute(cls, model_response, assistant):
        validated_response: Response = cls.parse_validate_response(model_response)
        return OutputResponse(
            success=True,
            raw_text=f"executing tv command: \
            {validated_response.action} > {validated_response.entity}",
        )
