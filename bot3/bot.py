import datetime
import ssl
import asyncio
import logging
import os
import json
import subprocess
from threading import Event
import requests
from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
from requests.packages.urllib3.exceptions import InsecureRequestWarning # pylint: disable=import-error
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from config import conf

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

BOT_TOKEN = conf['bot_token']
SOCKET_TOKEN = conf['bot_socket']
BOTNAME = 'bot'

ALLOW_USERS = ['U05K140HSUQ','']

SLACK_CLIENT = SocketModeClient(
    # This app-level token will be used only for establishing a connection
    app_token=SOCKET_TOKEN,  # xapp-A111-222-xyz
    # You will be using this AsyncWebClient for performing Web API calls in listeners
    web_client=WebClient(token=BOT_TOKEN, ssl=ssl_context)  # xoxb-111-222-xyz
)

from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest

def process(client: SocketModeClient, req: SocketModeRequest):
    if req.type == "events_api":
        # Acknowledge the request anyway
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)

        # Add a reaction to the message if it's a new message
        if req.payload["event"]["type"] == "message" \
            and req.payload["event"].get("subtype") is None:
            client.web_client.reactions_add(
                name="eyes",
                channel=req.payload["event"]["channel"],
                timestamp=req.payload["event"]["ts"],
            )
    if req.type == "interactive" \
        and req.payload.get("type") == "shortcut":
        if req.payload["callback_id"] == "hello-shortcut":
            # Acknowledge the request
            response = SocketModeResponse(envelope_id=req.envelope_id)
            client.send_socket_mode_response(response)
            # Open a welcome modal
            client.web_client.views_open(
                trigger_id=req.payload["trigger_id"],
                view={
                    "type": "modal",
                    "callback_id": "hello-modal",
                    "title": {
                        "type": "plain_text",
                        "text": "Greetings!"
                    },
                    "submit": {
                        "type": "plain_text",
                        "text": "Good Bye"
                    },
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "Hello!"
                            }
                        }
                    ]
                }
            )

    if req.type == "interactive" \
        and req.payload.get("type") == "view_submission":
        if req.payload["view"]["callback_id"] == "hello-modal":
            # Acknowledge the request and close the modal
            response = SocketModeResponse(envelope_id=req.envelope_id)
            client.send_socket_mode_response(response)

if __name__ == "__main__":
    try:
        #rtm.start()
        # Add a new listener to receive messages from Slack
        # You can add more listeners like this
        SLACK_CLIENT.socket_mode_request_listeners.append(process)
        # Establish a WebSocket connection to the Socket Mode servers
        SLACK_CLIENT.connect()
        # Just not to stop this process
        Event().wait()
    except Exception as main_e:
        error = str(main_e)
        logging.warning('main func: %s', error)