from .app import app
from .MisterMarketBot import MisterMarketBot


@app.event("app_mention")
def handle_message(event, say):
    app.logger.debug(f"event: {event}")
    user = event['user']
    message = event.get("text")
    app.logger.info(f"User: {user} Message {message}")
    bot = MisterMarketBot()
    response = bot.handle_slack_message(message)
    say(response)
