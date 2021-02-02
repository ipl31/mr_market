import pytest
from mister_market import stock_commands


@pytest.fixture
def price_command():
    return stock_commands.PriceCommand()


@pytest.fixture
def quote_command():
    return stock_commands.QuoteCommand()


@pytest.fixture
def indexes_command():
    return stock_commands.IndexesCommand()


@pytest.mark.skip(reason="needs to be fixed")
def test_quote_command_stock(quote_command):
    result = quote_command.run('AAPL')
    assert "AAPL" in result.text.join(" ")


@pytest.mark.skip(reason="needs to be fixed")
def test_quote_command_gold(quote_command):
    result = quote_command.run('GCUSD')
    assert "GCUSD" in result.text.text
    # test both gold symbol alias and lowercase:
    result = quote_command.run('xauusd')
    assert "GCUSD" in result.text.join(" ")


def test_price_command_stock(price_command):
    result = price_command.run('AAPL')
    symbol, price = result[0].text.text.split()
    assert "AAPL" in symbol


def test_price_command_crypto(price_command):
    result = price_command.run('BTCUSD')
    symbol, price = result[0].text.text.split()
    assert "BTCUSD" in symbol


@pytest.mark.skip(reason="needs to be fixed")
def test_index_command(indexes_command):
    result = indexes_command.run()
    assert "GSPC" in result.text.join(" ")
