import logging
import os
from slack_bolt import App


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Staring python logger in main.py")
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

app.logger.debug("Starting Mr. Market Flask App")