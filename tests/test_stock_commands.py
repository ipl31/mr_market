import pytest
from slackblocks import DividerBlock, HeaderBlock, SectionBlock
from mister_market import stock_commands


@pytest.fixture
def price_command():
    return stock_commands.PriceCommand()


@pytest.fixture
def quote_command():
    return stock_commands.QuoteCommand()


def test_quote_command_stock(quote_command):
    result = quote_command.run('AAPL')
    assert isinstance(result[0], HeaderBlock)
    assert isinstance(result[1], DividerBlock)
    assert isinstance(result[2], SectionBlock)
    assert "AAPL" in result[0].text.text


def test_quote_command_gold(quote_command):
    result = quote_command.run('GCUSD')
    assert isinstance(result[0], HeaderBlock)
    assert isinstance(result[1], DividerBlock)
    assert isinstance(result[2], SectionBlock)
    assert "GCUSD" in result[0].text.text
    # test both gold symbol alias and lowercase:
    result = quote_command.run('xauusd')
    assert "GCUSD" in result[0].text.text


def test_price_command_stock(price_command):
    result = price_command.run('AAPL')
    symbol, price = result[0].text.text.split()
    assert "AAPL" in symbol


def test_price_command_crypto(price_command):
    result = price_command.run('BTCUSD')
    symbol, price = result[0].text.text.split()
    assert "BTCUSD" in symbol
