import logging
import os
from flask import Flask
from slackeventsapi import SlackEventAdapter
from slack import WebClient

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

events_token = os.environ.get("SLACK_EVENTS_TOKEN")
client_token = os.environ.net("SLACK_TOKEN")

if events_token is None or client_token is None:
    raise KeyError("Slack tokens not set")

slack_events_adapter = SlackEventAdapter(events_token, "/slack/events", app)
slack_web_client = WebClient(token=client_token)


@app.route("/")
def hello():
    return "Hello"


@slack_events_adapter.on("message")
def handle_message(data):
    """ Handle slack message events """
    app.logger.debug('Handling slack message event.')
    return None
