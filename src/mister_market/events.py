from slackblocks import Message
from .app import app
from .MisterMarketBot import MisterMarketBot


@app.event("app_mention")
def handle_message(event, say):
    app.logger.debug(f"event: {event}")
    user = event['user']
    channel = event['channel']
    message = event.get("text")
    app.logger.info(f"User: {user} Message {message}")
    bot = MisterMarketBot()
    response_blocks = bot.handle_slack_message(message)
    message = Message(channel=channel, blocks=response_blocks)
    say(**message)
