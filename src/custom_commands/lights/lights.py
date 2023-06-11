import json
from base_command.base_command import BaseCommand
from custom_commands.lights.response import Response
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

        light = process.extractOne(
            f"light.{validated_response.entity}",
            all_lights.keys(),
            scorer=fuzz.token_set_ratio,
            score_cutoff=60,
        )

        if light is None:
            return OutputResponse(
                success=False,
                raw_text=f"Could not find any lights named {validated_response.entity}",
            )

        cls.switch_light(light[0], validated_response.action)

        return OutputResponse(
            success=True,
            raw_text="",
        )

    @staticmethod
    def get_lights():
        url = f"{config.HOME_ASSISTANT_ADDRESS}/api/states"
        response = requests.get(url, headers=HEADERS, timeout=5)

        if response.status_code != 200:
            raise requests.HTTPError("Failed to reach home assistant")

        entities = response.json()
        return {
            e["entity_id"]: {
                "name": e["attributes"]["friendly_name"],
                "state": e["state"],
            }
            for e in entities
            if e["entity_id"].startswith("light.")
        }

    @staticmethod
    def switch_light(light_id, action):
        state = "on" if action else "off"
        url = f"{config.HOME_ASSISTANT_ADDRESS}/api/services/light/turn_{state}"
        payload = {"entity_id": light_id}
        response = requests.post(
            url, headers=HEADERS, data=json.dumps(payload), timeout=5
        )
        if response.status_code != 200:
            raise requests.HTTPError("Failed to reach home assistant")
