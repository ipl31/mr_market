import logging
import os
from slack_bolt import App
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Staring python logger in main.py")

token = os.environ["SLACK_BOT_TOKEN"]
signing_secret = os.environ["SLACK_SIGNING_SECRET"]

oauth_settings = OAuthSettings(
    client_id=os.environ["SLACK_CLIENT_ID"],
    client_secret=os.environ["SLACK_CLIENT_SECRET"],
    scopes=["channels:read", "groups:read", "chat:write"],
    # This is temporary. Need to migrate to S3 or something.
    installation_store=FileInstallationStore(base_dir="./data"),
    state_store=FileOAuthStateStore(expiration_seconds=600, base_dir="./data")
)


app = App(
    # Remove when done testing oauth.
    token=token,
    signing_secret=signing_secret,
    oauth_settings=oauth_settings
)

app.logger.debug("Starting Mr. Market Flask App")
