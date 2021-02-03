import pytest
from mister_market.constants import (MisterMarketConstants,
                                     ConstantError)


def test_constants():
    constants = MisterMarketConstants()
    with pytest.raises(ConstantError):
        constants.FMP_GOLD_SYMBOL = "foo"
