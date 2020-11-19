import logging
import os
from iexfinance.stocks import Stock
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
slack_client = WebClient(token=client_token)


def create_message_block(text):
    msg_block = {
                "type": "section",
                "text": {"type": "mrkdwn", "text": (f"{text}\n\n"),
                         },
                }
    return msg_block


def post_message(channel_id, text):
    block = create_message_block(text)
    message = {"channel": channel_id,
               "blocks": [block],
               }
    slack_client.chat_postMessage(**message)


@app.route("/")
def hello():
    return "Hello"


@slack_events_adapter.on("message")
def handle_message(data):
    """ Handle slack message events """
    app.logger.debug("Handling slack message event.")
    bot_id = slack_client.api_call("auth.test")['user_id']
    event = data.get("event", {})
    user_id = event.get("user")
    text = event.get("text")
    channel_id = event.get("channel")

    if bot_id == user_id:
        app.logger.debug("Message is from myself, skipping.")
        return
    if bot_id not in text:
        app.logger.debug("Message is not addressed to me. Skipping")
        return

    if "hello" in text.lower():
        post_message(channel_id, "Hello!")
        return

    if "price" in text.lower():
        message_list = text.split()
        symbol = message_list[2]
        try:
            stock = Stock(symbol).get_price()
            price = stock.get_price()
            message = f"Symbol: {symbol}  Price: {price}"
            post_message(channel_id, message)
        except Exception:
            post_message(channel_id, f"I encountered an error for {symbol}")
            return
        return
