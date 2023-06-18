import asyncio
import base64
import codecs
import json
import os
import websockets
import logging

logger = logging.getLogger(__name__)

from .endpoints import *

KEY_FILE_NAME = ".pylgtv"
USER_HOME = "HOME"
HANDSHAKE_FILE_NAME = "handshake.json"


class PyLGTVPairException(Exception):
    def __init__(self, message):
        self.message = message


class WebOsClient(object):
    def __init__(self, ip, key_file_path=None, timeout_connect=10):
        """Initialize the client."""
        self.ip = ip
        self.port = 3000
        self.key_file_path = key_file_path
        self.client_key = None
        self.web_socket = None
        self.command_count = 0
        self.last_response = None
        self.timeout_connect = timeout_connect

        self.load_key_file()

    @staticmethod
    def _get_key_file_path():
        """Return the key file path."""
        if os.getenv(USER_HOME) is not None and os.access(
            os.getenv(USER_HOME), os.W_OK
        ):
            return os.path.join(os.getenv(USER_HOME), KEY_FILE_NAME)

        return os.path.join(os.getcwd(), KEY_FILE_NAME)

    def load_key_file(self):
        """Try to load the client key for the current ip."""
        self.client_key = None
        if self.key_file_path:
            key_file_path = self.key_file_path
        else:
            key_file_path = self._get_key_file_path()
        key_dict = {}

        logger.debug("load keyfile from %s", key_file_path)

        if os.path.isfile(key_file_path):
            with open(key_file_path, "r") as f:
                raw_data = f.read()
                if raw_data:
                    key_dict = json.loads(raw_data)

        logger.debug("getting client_key for %s from %s", self.ip, key_file_path)
        if self.ip in key_dict:
            self.client_key = key_dict[self.ip]

    def save_key_file(self):
        """Save the current client key."""
        if self.client_key is None:
            return

        if self.key_file_path:
            key_file_path = self.key_file_path
        else:
            key_file_path = self._get_key_file_path()

        logger.debug("save keyfile to %s", key_file_path)

        with open(key_file_path, "w+") as f:
            raw_data = f.read()
            key_dict = {}

            if raw_data:
                key_dict = json.loads(raw_data)

            key_dict[self.ip] = self.client_key

            f.write(json.dumps(key_dict))

    async def _send_register_payload(self, websocket):
        file = os.path.join(os.path.dirname(__file__), HANDSHAKE_FILE_NAME)

        data = codecs.open(file, "r", "utf-8")
        raw_handshake = data.read()

        handshake = json.loads(raw_handshake)
        handshake["payload"]["client-key"] = self.client_key

        await websocket.send(json.dumps(handshake))
        raw_response = await websocket.recv()
        response = json.loads(raw_response)

        if (
            response["type"] == "response"
            and response["payload"]["pairingType"] == "PROMPT"
        ):
            raw_response = await websocket.recv()
            response = json.loads(raw_response)
            if response["type"] == "registered":
                self.client_key = response["payload"]["client-key"]
                self.save_key_file()

    def is_registered(self):
        return self.client_key is not None

    async def _register(self):
        logger.debug("register on %s", "ws://{}:{}".format(self.ip, self.port))
        try:
            websocket = await websockets.connect(
                "ws://{}:{}".format(self.ip, self.port), timeout=self.timeout_connect
            )

        except:
            logger.error(
                "register failed to connect to %s",
                "ws://{}:{}".format(self.ip, self.port),
            )
            return False

        logger.debug(
            "register websocket connected to %s",
            "ws://{}:{}".format(self.ip, self.port),
        )

        try:
            await self._send_register_payload(websocket)

        finally:
            logger.debug(
                "close register connection to %s",
                "ws://{}:{}".format(self.ip, self.port),
            )
            await websocket.close()

    def register(self):
        """Pair client with tv."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._register())

    async def _command(self, msg):
        """Send a command to the tv."""
        logger.debug("send command to %s", "ws://{}:{}".format(self.ip, self.port))
        try:
            websocket = await websockets.connect(
                "ws://{}:{}".format(self.ip, self.port), timeout=self.timeout_connect
            )
        except:
            logger.debug(
                "command failed to connect to %s",
                "ws://{}:{}".format(self.ip, self.port),
            )
            return False

        logger.debug(
            "command websocket connected to %s", "ws://{}:{}".format(self.ip, self.port)
        )

        try:
            await self._send_register_payload(websocket)

            if not self.client_key:
                raise PyLGTVPairException("Unable to pair")

            await websocket.send(json.dumps(msg))

            if msg["type"] == "request":
                raw_response = await websocket.recv()
                self.last_response = json.loads(raw_response)

        finally:
            logger.debug(
                "close command connection to %s",
                "ws://{}:{}".format(self.ip, self.port),
            )
            await websocket.close()

    def command(self, request_type, uri, payload):
        self.command_count += 1

        if payload is None:
            payload = {}

        message = {
            "id": "{}_{}".format(type, self.command_count),
            "type": request_type,
            "uri": "ssap://{}".format(uri),
            "payload": payload,
        }

        self.last_response = None

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(
                asyncio.wait_for(self._command(message), self.timeout_connect)
            )
        finally:
            loop.close()

    def request(self, uri, payload=None):
        self.command("request", uri, payload)

    def send_message(self, message, icon_path=None):
        icon_encoded_string = ""
        icon_extension = ""

        if icon_path is not None:
            icon_extension = os.path.splitext(icon_path)[1][1:]
            with open(icon_path, "rb") as icon_file:
                icon_encoded_string = base64.b64encode(icon_file.read()).decode("ascii")

        self.request(
            EP_SHOW_MESSAGE,
            {
                "message": message,
                "iconData": icon_encoded_string,
                "iconExtension": icon_extension,
            },
        )

    def get_apps(self):
        self.request(EP_GET_APPS)
        return (
            {}
            if self.last_response is None
            else self.last_response.get("payload").get("launchPoints")
        )

    def get_current_app(self):
        self.request(EP_GET_CURRENT_APP_INFO)
        return (
            None
            if self.last_response is None
            else self.last_response.get("payload").get("appId")
        )

    def launch_app(self, app):
        self.command("request", EP_LAUNCH, {"id": app})

    def launch_app_with_params(self, app, params):
        self.request(EP_LAUNCH, {"id": app, "params": params})

    def launch_app_with_content_id(self, app, contentId):
        self.request(EP_LAUNCH, {"id": app, "contentId": contentId})

    def close_app(self, app):
        self.request(EP_LAUNCHER_CLOSE, {"id": app})

    # Services
    def get_services(self):
        self.request(EP_GET_SERVICES)
        return (
            {}
            if self.last_response is None
            else self.last_response.get("payload").get("services")
        )

    def get_software_info(self):
        self.request(EP_GET_SOFTWARE_INFO)
        return {} if self.last_response is None else self.last_response.get("payload")

    def power_off(self):
        self.request(EP_POWER_OFF)

    def power_on(self):
        self.request(EP_POWER_ON)

    def turn_3d_on(self):
        self.request(EP_3D_ON)

    def turn_3d_off(self):
        self.request(EP_3D_OFF)

    # Inputs
    def get_inputs(self):
        self.request(EP_GET_INPUTS)
        return (
            {}
            if self.last_response is None
            else self.last_response.get("payload").get("devices")
        )

    def get_input(self):
        return self.get_current_app()

    def set_input(self, input):
        self.request(EP_SET_INPUT, {"inputId": input})

    # Audio
    def get_audio_status(self):
        self.request(EP_GET_AUDIO_STATUS)
        return {} if self.last_response is None else self.last_response.get("payload")

    def get_muted(self):
        return self.get_audio_status().get("mute")

    def set_mute(self, mute):
        self.request(EP_SET_MUTE, {"mute": mute})

    def get_volume(self):
        self.request(EP_GET_VOLUME)
        return (
            0
            if self.last_response is None
            else self.last_response.get("payload").get("volume")
        )

    def set_volume(self, volume):
        volume = max(0, volume)
        self.request(EP_SET_VOLUME, {"volume": volume})

    def volume_up(self):
        self.request(EP_VOLUME_UP)

    def volume_down(self):
        self.request(EP_VOLUME_DOWN)

    # TV Channel
    def channel_up(self):
        self.request(EP_TV_CHANNEL_UP)

    def channel_down(self):
        self.request(EP_TV_CHANNEL_DOWN)

    def get_channels(self):
        self.request(EP_GET_TV_CHANNELS)
        return (
            {}
            if self.last_response is None
            else self.last_response.get("payload").get("channelList")
        )

    def get_current_channel(self):
        self.request(EP_GET_CURRENT_CHANNEL)
        return {} if self.last_response is None else self.last_response.get("payload")

    def get_channel_info(self):
        self.request(EP_GET_CHANNEL_INFO)
        return {} if self.last_response is None else self.last_response.get("payload")

    def set_channel(self, channel):
        self.request(EP_SET_CHANNEL, {"channelId": channel})

    def play(self):
        self.request(EP_MEDIA_PLAY)

    def pause(self):
        self.request(EP_MEDIA_PAUSE)

    def stop(self):
        self.request(EP_MEDIA_STOP)

    def close(self):
        self.request(EP_MEDIA_CLOSE)

    def rewind(self):
        self.request(EP_MEDIA_REWIND)

    def fast_forward(self):
        self.request(EP_MEDIA_FAST_FORWARD)

    # Keys
    def send_enter_key(self):
        self.request(EP_SEND_ENTER)

    def send_delete_key(self):
        self.request(EP_SEND_DELETE)

    # Web
    def open_url(self, url):
        self.request(EP_OPEN, {"target": url})

    def close_web(self):
        self.request(EP_CLOSE_WEB_APP)
