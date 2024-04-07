from pathlib import Path
from base_command.base_command import BaseCommand
from config import config
from custom_commands.tv_control.response import Response
from custom_commands.tv_control.webos_client.endpoints import (
    EP_MEDIA_PAUSE,
    EP_MEDIA_PLAY,
    EP_MEDIA_STOP,
    EP_SET_INPUT,
    EP_SET_MUTE,
    EP_VOLUME_DOWN,
    EP_VOLUME_UP,
)
from custom_commands.tv_control.webos_client.webos_client import WebOsClient
from output.output_response import OutputResponse
from fuzzywuzzy import process
from fuzzywuzzy import fuzz


class TvControl(BaseCommand):
    @classmethod
    def execute(cls, model_response, assistant):
        cls.TV = WebOsClient(
            config.TV_IP, key_file_path=f"{Path(__file__).parent}/.pylgtv"
        )
        validated_response: Response = cls.parse_validate_response(model_response)
        try:
            cls.execute_command(validated_response)

            return OutputResponse(success=True)
        except Exception as e:
            config.logger.error(e)
            return OutputResponse(success=False)

    @classmethod
    def execute_command(cls, response: Response):
        getattr(cls, response.action)(response)

    @classmethod
    def power(cls, response: Response):
        if response.entity == "off":
            cls.TV.power_off()
        else:
            cls.TV.power_on()

    @classmethod
    def volume(cls, response: Response):
        if response.entity.isnumeric():
            cls.TV.set_volume(int(response.entity))
            return
        if response.entity == "mute":
            cls.TV.set_mute(True)
            return

        volume_cmd = {
            "up": EP_VOLUME_UP,
            "down": EP_VOLUME_DOWN,
        }
        cls.TV.request(volume_cmd[response.entity.lower()])

    @classmethod
    def app(cls, response: Response):
        apps = {app["title"].lower(): app["id"] for app in cls.get_available_apps()}
        chosen_app = process.extractOne(
            response.entity.lower(),
            apps.keys(),
            scorer=fuzz.token_set_ratio,
            score_cutoff=60,
        )

        cls.TV.launch_app(apps[chosen_app[0]])

    @classmethod
    def control(cls, response: Response):
        control = {
            "pause": EP_MEDIA_PAUSE,
            "play": EP_MEDIA_PLAY,
            "stop": EP_MEDIA_STOP,
        }
        cls.TV.request(control[response.entity.lower()])

    @classmethod
    def input(cls, response: Response):
        input = config.TV_INPUTS.get(response.entity.lower())
        if input:
            cls.TV.launch_app(f"com.webos.app.{input.lower()}")

    @classmethod
    def get_available_apps(cls) -> dict:
        return cls.TV.get_apps()
