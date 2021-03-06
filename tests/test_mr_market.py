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


@pytest.mark.skip(msg="Need to figure out to test this with new resolver.")
def test_handle_slack_message_bad_command(bot):
    result = bot.handle_slack_message("not a command")
    assert "I don't understand your command" in result[0].text.text


def test_handle_slack_message_btc(bot):
    result = bot.handle_slack_message("@1234 price btc")
    symbol, price = result[0].text.text.split()
    assert "BTCUSD" in symbol[1:-1]
    assert isinstance(float(price[1:-1]), float)

    result = bot.handle_slack_message("@1234 price BTC")
    symbol, price = result[0].text.text.split()
    assert "BTCUSD" in symbol[1:-1]
    assert isinstance(float(price[1:-1]), float)

    result = bot.handle_slack_message("@1234 price ETHUSD")
    symbol, price = result[0].text.text.split()
    assert symbol[1:-1] == "ETHUSD"
    assert isinstance(float(price[1:-1]), float)


def test_handle_slack_message_aapl(bot):
    result = bot.handle_slack_message("@1234 price AAPL")
    symbol, price = result[0].text.text.split()
    assert symbol[1:-1] == "AAPL"
    assert isinstance(float(price[1:-1]), float)

    result = bot.handle_slack_message("@1234 price aapl")
    symbol, price = result[0].text.text.split()
    assert symbol[1:-1] == "AAPL"
    assert isinstance(float(price[1:-1]), float)
