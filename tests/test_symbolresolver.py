import pytest
from mister_market.constants import MisterMarketConstants
from mister_market.SymbolResolver import SymbolResolver


@pytest.fixture
def resolver():
    return SymbolResolver()


@pytest.fixture
def constants():
    return MisterMarketConstants()


def test_symbol_resolver(resolver, constants):
    assert resolver.symbol_resolve('asdasdasfasfasfasfa') is None
    assert resolver.symbol_resolve('AAPL') == ('AAPL',
                                               constants.DATA_SOURCE_FMP,
                                               constants.STOCK)
    assert resolver.fuzzy_symbol_lookup('Apple') == ('AAPL')
    assert resolver.fuzzy_symbol_lookup('asdaskljfsdkljfas;ldkfja') is None
