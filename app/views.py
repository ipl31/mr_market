import logging
import os
from . import app
from slackeventsapi import SlackEventAdapter
from slack import WebClient

logging.basicConfig(level=logging.DEBUG)
# TODO: Tokens should be in app.config
events_token = os.environ.get("SLACK_EVENTS_TOKEN")
client_token = os.environ.get("SLACK_TOKEN")

if events_token is None or client_token is None:
    raise KeyError("Slack tokens not set")

slack_events_adapter = SlackEventAdapter(events_token, "/slack/events", app)
slack_web_client = WebClient(token=client_token)
bot_id = client.api_call("auth.test")['user_id']
message_count = {}


@app.route("/")
def hello():
    return "Hello"


@slack_events_adapter.on("message")
def handle_message(data):
    """ Handle slack message events """
    app.logger.debug("Handling slack message event.")
    event = data.get("event", {})
    user_id = event.get("user")
    text = event.get("text")
    channel_id = event.get("channel")
    if bot_id == user_id:
        app.logger.debug("Message is from myself, skipping.")
        return None
    app.logger.debug(f"event: {event}")
    return None
