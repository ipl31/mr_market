import logging
import os

from flask import Flask
from slackeventsapi import SlackEventAdapter
from slack import WebClient

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

slack_events_adapter = SlackEventAdapter(os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", app)
slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))

@slack_events_adapter.on("message")
def handle_message(data):
    """ Handle slack message events """
    app.logger.debug('Handling slack message event.')
    return None

if __name__ == '__main__':
    app.run()
