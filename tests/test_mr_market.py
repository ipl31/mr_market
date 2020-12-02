import pytest
from mister_market.MisterMarketBot import MisterMarketBot


@pytest.fixture
def bot():
    return MisterMarketBot()


def test_parse_command(bot):
    command, args = \
        bot._parse_command("test_command param1 param2")
    assert command == "test_command"
    assert args == ["param1", "param2"]


def test_handle_slack_message(bot):
    result = bot.handle_slack_message("not a command")
    assert "I do not understand your command" in result
