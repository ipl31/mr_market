import logging
import os
from iexfinance.stocks import Stock
from iexfinance.altdata import get_social_sentiment
from . import app
from slackeventsapi import SlackEventAdapter
from slack import WebClient

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
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
    logger.debug("Handling slack message event.")
    bot_id = slack_client.api_call("auth.test")['user_id']
    event = data.get("event", {})
    user_id = event.get("user")
    text = event.get("text")
    channel_id = event.get("channel")

    if bot_id == user_id:
        logger.debug("Message is from myself, skipping.")
        return
    if bot_id not in text:
        logger.debug("Message is not addressed to me. Skipping")
        return

    tokenized_message = text.lower().split()
    maybe_command = text.lower()[1]

    if maybe_command == "hello":
        post_message(channel_id, "Hello!")
        return

    if maybe_command == "sentiment":
        symbol = tokenized_message[2]
        sentiment_data = get_social_sentiment(symbol)
        sentiment = sentiment_data["sentiment"]
        scores = sentiment_data["scores"]
        positive = sentiment_data["positive"]
        negative = sentiment_data["negative"]
        msg = (f"Symbol:`{symbol}` Sentiment:`{sentiment}`"
               "Scores:`{scores}` Positive:`{positive}` Negative:`{negative}`")
        post_message(channel_id, msg)

    if maybe_command == "stock":
        maybe_sub_command = tokenized_message[1]
        if maybe_sub_command == "sentiment":
            maybe_symbol = tokenized_message[2]
            try:
                sentiment_data = get_social_sentiment(maybe_symbol)
            except Exception:
                msg = f"I encountered and error getting sentiment for {symbol}"
                logger.exception(msg)
                post_message(channel_id, msg)
                return

            sentiment = sentiment_data["sentiment"]
            scores = sentiment_data["scores"]
            positive = sentiment_data["positive"]
            negative = sentiment_data["negative"]
            message = f"Symbol:`{symbol}` Sentiment:`{sentiment}`" \
                      f" Scores:`{scores}` Positive:`{positive}`" \
                      f" Negative:`{negative}`"
            post_message(channel_id, message)

        if maybe_sub_command == "price":
            symbol = tokenized_message[2]
            try:
                stock = Stock(symbol)
                price = stock.get_price()
                message = f"Symbol: `{symbol}`  Price: `{price}`"
                post_message(channel_id, message)
            except Exception:
                logger.exception("Error getting stock price")
                post_message(channel_id,
                             f"I encountered an error for `{symbol}`")
                return
            return

    msg = ('I don\'t understand your request.'
           ' I understand "stock price $symbol",'
           '"stock quote $symbol", "stock sentiment $symbol" and "hello"')
    post_message(channel_id, msg)
