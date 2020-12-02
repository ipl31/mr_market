from mister_market import stock_commands


def test_is_symbol_in_iex_universe():
    aapl_result = stock_commands.is_symbol_in_iex_universe("AAPL")
    assert aapl_result is True
    fake_result = stock_commands.is_symbol_in_iex_universe("ASDAFASD")
    assert fake_result is False
