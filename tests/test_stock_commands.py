import pytest
from mister_market import stock_commands


@pytest.fixture
def price_command():
    return stock_commands.PriceCommand()


@pytest.fixture
def quote_command():
    return stock_commands.QuoteCommand()


def test_is_symbol_in_iex_universe():
    aapl_result = stock_commands.is_symbol_in_iex_universe("AAPL")
    assert aapl_result is True
    fake_result = stock_commands.is_symbol_in_iex_universe("ASDAFASD")
    assert fake_result is False


def test_price_command_stock(price_command):
    result = price_command.run('AAPL')
    symbol, price = result.split()
    assert "AAPL" in symbol


def test_price_command_crypto(price_command):
    result = price_command.run('BTCUSD')
    symbol, price = result.split()
    assert "BTCUSD" in symbol
