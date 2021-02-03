from mister_market import helpers


def test_get_fmp_quote():
    result = helpers.get_fmp_quote('GCUSD')
    assert 'GCUSD' in result['symbol']


def test_get_fmp_stock_symbol_universe():
    result = helpers.get_fmp_stock_symbol_universe()
    assert any(['SPY' in [s['symbol'] for s in result]])


def test_get_gold_price():
    assert isinstance(helpers.get_gold_price(), float)


def test_commaify():
    assert "100,000" == helpers.commaify(100000)
    assert "1,000,000.51" == helpers.commaify(1000000.51)


def test_is_symbol_in_iex_universe():
    aapl_result = helpers.is_symbol_in_iex_universe("AAPL")
    assert aapl_result is True
    fake_result = helpers.is_symbol_in_iex_universe("ASDAFASD")
    assert fake_result is False
