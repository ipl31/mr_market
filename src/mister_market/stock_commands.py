from functools import lru_cache
from iexfinance import altdata, refdata
from iexfinance.stocks import Stock
from iexfinance.utils.exceptions import IEXQueryError
from slackblocks import HeaderBlock, DividerBlock, SectionBlock
from .plugin_base import PluginBase


@lru_cache(maxsize=1)
def get_iex_symbol_universe():
    return refdata.get_symbols()


def is_symbol_in_iex_universe(symbol):
    for entry in get_iex_symbol_universe():
        if symbol == entry['symbol']:
            return True
    return False


class QuoteCommand(PluginBase):

    command = "quote"
    usage = "quote $symbol"
    description = "Quote including data beyond price."

    def __init__(self):
        pass

    @staticmethod
    def _build_quote_msg_block(quote):
        blocks = []

        symbol = quote.get("symbol")
        name = quote.get("companyName")
        price = quote.get("latestPrice")
        market_cap = quote.get("marketCap")
        volume = quote.get("volume")
        avg_volume = quote.get("avgTotalVolume")
        pe = quote.get("peRatio")
        high52 = quote.get("week52High")
        low52 = quote.get("week52Low")
        ytd = "{:.0%}".format(quote.get("ytdChange"))

        blocks.append(HeaderBlock(
            text=f"{symbol} - {name}"))
        blocks.append(DividerBlock())

        blocks.append(
                SectionBlock(
                    text=f"*Price:* {price} - *P/E:* {pe}"))
        blocks.append(DividerBlock())

        blocks.append(
                SectionBlock(
                    text=(f"*Market cap:* {market_cap} - "
                          f"*Volume:* {volume} - *Avg*: {avg_volume}")))
        blocks.append(DividerBlock())

        blocks.append(SectionBlock(
            text=f"*52 High:* {high52} - *52w Low:* {low52} - *Ytd:* {ytd}"))

        return blocks

    def _get_stock_quote_blocks(self, symbol):
        quote = Stock(symbol).get_quote()
        blocks = self._build_quote_msg_block(quote)
        return blocks

    def run(self, *args, **kwargs):
        args = list(args)
        symbol = args.pop(0)
        symbol_err = f"Symbol `{symbol}` not found"

        if is_symbol_in_iex_universe(symbol):
            blocks = self._get_stock_quote_blocks(symbol)
            return blocks

        return symbol_err


class PriceCommand(PluginBase):

    command = "price"
    usage = "price $symbol"
    description = "Retrieve a price for a supported symbol."

    def __init__(self):
        pass

    @staticmethod
    def _get_stock_price(symbol):
        return Stock(symbol).get_price()

    @staticmethod
    def _get_crypto_price(symbol):
        if symbol.lower() == "btc":
            symbol = "BTCUSD"
        quote = altdata.get_crypto_quote(symbol)
        price = quote['latestPrice']
        return price

    def run(self, *args, **kwargs):
        args = list(args)
        symbol = args.pop(0)
        symbol_err = f"Symbol `{symbol}` not found"
        if is_symbol_in_iex_universe(symbol):
            price = self._get_stock_price(symbol)
            return SectionBlock(text=f"`{symbol}` `{price}`")
        try:
            price = self._get_crypto_price(symbol)
            if price is None:
                return SectionBlock(text=symbol_err)
            return SectionBlock(text=f"`{symbol}` `{price}`")
        except IEXQueryError:
            return SectionBlock(text=symbol_err)
