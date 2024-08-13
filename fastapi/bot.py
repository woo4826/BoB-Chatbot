import datetime
import ssl
import logging
from threading import Event
import requests
from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import vt
from config import config
from typing import Union, Dict

# Disable SSL warnings
urllib3.disable_warnings(InsecureRequestWarning)

# Configure SSL context
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Slack configuration
BOT_TOKEN = config['bot_token']
SOCKET_TOKEN = config['bot_socket']
ALLOW_USERS = ['U03C7RT9GA1']

# Initialize Slack client
SLACK_CLIENT = SocketModeClient(
    app_token=SOCKET_TOKEN,
    web_client=WebClient(token=BOT_TOKEN, ssl=ssl_context)
)

# Helper functions
def is_allowed_user(user_id: str) -> bool:
    """Check if the user is allowed."""
    return user_id in ALLOW_USERS

def send_slack_message(client: WebClient, channel: str,thread_ts: Union[str, None] = None, timestamp: Union[str, None] = None, text: str = "") -> None:
    """Send a message to Slack."""
    try:
        client.chat_postMessage(
            text=text,
            channel=channel,
            thread_ts=timestamp,
            timestamp=timestamp
        )
    except Exception as e:
        logging.warning('Error sending Slack message: %s', str(e))

def process_message(client: SocketModeClient, req: SocketModeRequest) -> None:
    """Process a message event."""
    event = req.payload["event"]
    user_id = event["user"]
    channel = event["channel"]
    message_text = event["text"]
    timestamp = event["ts"]
    thread_ts = event['event_ts'] 
    if not is_allowed_user(user_id):
        return
    
    if "ioc" not in message_text:
        return
    
    target_ip = message_text.split('ioc')[1].strip()
    try:
        vt_res = vt.virustotal(target_ip, 'ip')
        send_slack_message(client = client.web_client, channel=channel,thread_ts=thread_ts, timestamp=timestamp, text= str(vt_res))
        payload = {
            "access_user_id": user_id,
            "access_ch_id": channel,
            "message_text": message_text,
            "access_time": datetime.datetime.fromtimestamp(float(timestamp)).strftime('%Y-%m-%d %H:%M:%S'),
        }
        print(payload)
        post_res = requests.post('http://localhost:3000/ioc/log/create',  json=payload)
        logging.info('Posted to API: %s', post_res)
    except Exception as e:
        send_slack_message(client = client.web_client, channel=channel,thread_ts=thread_ts, timestamp=timestamp, text= 'Error processing the request')
        logging.warning('Process message error: %s', str(e))

def process_interactive_request(client: SocketModeClient, req: SocketModeRequest) -> None:
    """Process an interactive request."""
    if req.payload.get("type") == "shortcut" and req.payload["callback_id"] == "hello-shortcut":
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)
        client.web_client.views_open(
            trigger_id=req.payload["trigger_id"],
            view={
                "type": "modal",
                "callback_id": "hello-modal",
                "title": {"type": "plain_text", "text": "Greetings!"},
                "submit": {"type": "plain_text", "text": "Good Bye"},
                "blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": "Hello!"}}]
            }
        )
    elif req.payload.get("type") == "view_submission" and req.payload["view"]["callback_id"] == "hello-modal":
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)

def process(client: SocketModeClient, req: SocketModeRequest) -> None:
    """Process a request based on its type."""
    if req.type == "events_api":
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)
        if req.payload["event"]["type"] == "message" and req.payload["event"].get("subtype") is None:
            process_message(client, req)
    elif req.type == "interactive":
        process_interactive_request(client, req)

# Main entry point
if __name__ == "__main__":
    try:
        SLACK_CLIENT.socket_mode_request_listeners.append(process)
        SLACK_CLIENT.connect()
        Event().wait()
    except Exception as e:
        logging.warning('Main function error: %s', str(e))