from functools import lru_cache
# from iexfinance.stocks import Stock
from iexfinance import altdata, refdata
from iexfinance.stocks import Stock
from iexfinance.utils.exceptions import IEXQueryError
from .plugin_base import PluginBase


@lru_cache(maxsize=1)
def get_iex_symbol_universe():
    return refdata.get_symbols()


def is_symbol_in_iex_universe(symbol):
    for entry in get_iex_symbol_universe():
        if symbol == entry['symbol']:
            return True
    return False


class PriceCommand(PluginBase):

    command = "price"
    usage = "price $symbol"
    description = "Retrieve a price for a supported symbol"

    def __init__(self):
        pass

    def _get_stock_price(self, symbol):
        return Stock(symbol).get_price()

    def _get_crypto_price(self, symbol):
        if symbol.lower() == "btc":
            symbol = "BTCUSD"
        quote = altdata.get_crypto_quote(symbol)
        price = quote['latestPrice']
        return price

    def run(self, *args, **kwargs):
        args = list(args)
        symbol = args.pop(0)
        if is_symbol_in_iex_universe(symbol):
            price = self._get_stock_price(symbol)
            return f"`{symbol}` `{price}`"
        try:
            price = self._get_crypto_price(symbol)
            if price is None:
                return f"Symbol `{symbol}` not found"
            return f"`{symbol}` `{price}`"
        except IEXQueryError:
            return f"Symbol `{symbol}` not found"
