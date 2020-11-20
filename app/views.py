import logging
import os
from iexfinance.stocks import Stock
from . import app
from .MisterMarketBot import MisterMarketBot
from slackeventsapi import SlackEventAdapter
from slack import WebClient

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# TODO: Tokens should be in app.config
events_token = os.environ.get("SLACK_EVENTS_TOKEN")
# TODO: Centralize client code in a module
client_token = os.environ.get("SLACK_TOKEN")
slack_client = WebClient(token=client_token)

if events_token is None or client_token is None:
    raise KeyError("Slack tokens not set")

slack_events_adapter = SlackEventAdapter(events_token, "/slack/events", app)


@app.route("/")
def hello():
    return "Hello"


@slack_events_adapter.on("message")
def handle_message(payload):
    bot_id = slack_client.api_call("auth.test")['user_id']
    skills = {"stock": Stock}
    bot = MisterMarketBot(skills, bot_id)
    bot.handle_slack_event(payload)
