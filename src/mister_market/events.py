from .app import app
from .iex_skills import IexStockSkill
from .MisterMarketBot import MisterMarketBot


@app.event("app_mention")
def handle_message(event, say):
    app.logger.debug(f"event: {event}")
    user = event['user']
    message = event.get("text")
    bot = MisterMarketBot(IexStockSkill())
    response = bot.handle_slack_message(message)
    say(response)