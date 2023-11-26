import json
from base_command.base_command import BaseCommand
from custom_commands.lights.response import LightStateEnum, Response
from output.output_response import OutputResponse
from config import config
import requests
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

HEADERS = {
    "Authorization": f"Bearer {config.HOME_ASSISTANT_KEY}",
    "content-type": "application/json",
}


class Lights(BaseCommand):
    @classmethod
    def execute(cls, model_response, assistant):
        validated_response: Response = cls.parse_validate_response(model_response)

        all_lights = cls.get_lights()

        if validated_response.entity.lower() == "all":
            all_lights_ids = [light["id"] for light in all_lights.values()]
            cls.switch_light(all_lights_ids, validated_response.action)
            return OutputResponse(
                success=True,
                raw_text="",
            )

        light_name = process.extractOne(
            validated_response.entity,
            all_lights.keys(),
            scorer=fuzz.token_set_ratio,
            score_cutoff=60,
        )

        if light_name is None:
            return OutputResponse(
                success=False,
                raw_text=f"Could not find any lights named {validated_response.entity}",
            )

        light_id = all_lights[light_name[0]].get("id")
        cls.switch_light([light_id], validated_response.action)

        return OutputResponse(
            success=True,
            raw_text="",
        )

    @staticmethod
    def get_lights():
        url = f"{config.HOME_ASSISTANT_ADDRESS}/api/states"
        try:
            response = requests.get(url, headers=HEADERS, timeout=5)

            if response.status_code != 200:
                raise ConnectionRefusedError("Failed to reach home assistant")
        except Exception as ex:
            raise ConnectionRefusedError("Failed to reach home assistant")

        entities = response.json()
        return {
            Lights.format_light_name(e["attributes"]["friendly_name"]): {
                "id": e["entity_id"],
                "state": e["state"],
            }
            for e in entities
            if e["entity_id"].startswith("light.")
        }

    @staticmethod
    def switch_light(lights_id: list[str], action: str):
        url = f"{config.HOME_ASSISTANT_ADDRESS}/api/services/light/turn_{action.value}"
        payload = {"entity_id": lights_id}
        config.logger.debug(payload)
        config.logger.debug(url)

        try:
            response = requests.post(
                url, headers=HEADERS, data=json.dumps(payload), timeout=5
            )
            if response.status_code != 200:
                raise ConnectionRefusedError("Failed to reach home assistant")
        except Exception as ex:
            raise ConnectionRefusedError("Failed to reach home assistant")

    @staticmethod
    def format_light_name(light: str) -> str:
        return "_".join(light.split(" "))
