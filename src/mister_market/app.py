import logging
import os
from slack_bolt import App


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Staring python logger in main.py")

token = os.environ.get("SLACK_BOT_TOKEN")
signing_secret = os.environ.get("SLACK_SIGNING_SECRET")

app = App(
    token=token,
    signing_secret=signing_secret
)

app.logger.debug("Starting Mr. Market Flask App")
