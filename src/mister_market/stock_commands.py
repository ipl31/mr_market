from functools import lru_cache
# from iexfinance.stocks import Stock
from iexfinance import refdata
from .plugin_base import PluginBase


@lru_cache(maxsize=1)
def get_iex_symbol_universe():
    return refdata.get_symbols()


def is_symbol_in_iex_universe(symbol):
    for entry in get_iex_symbol_universe():
        if symbol in entry['symbol']:
            return True
    return False


class PriceCommand(PluginBase):

    command = "price"
    usage = "price $symbol"
    description = "Retrieve a price for a supported symbol"

    def __init__(self):
        pass

    def run(self, *args, **kwargs):
        pass
