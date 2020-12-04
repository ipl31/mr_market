import os
import requests
from functools import lru_cache
from iexfinance import altdata, refdata
from iexfinance.stocks import Stock
from iexfinance.utils.exceptions import IEXQueryError
from slackblocks import HeaderBlock, DividerBlock, SectionBlock
from .plugin_base import PluginBase

GOLD_ALIASES = ["GCUSD", "XAUUSD", "XAU"]
GOLD_COMM_SYMBOL = "GCUSD"


@lru_cache(maxsize=1)
def get_iex_symbol_universe():
    return refdata.get_symbols()


def get_fmp_quote(symbol):
    key = os.environ.get("FMP_API_KEY")
    url = "https://financialmodelingprep.com/api/v3/quote"
    response = requests.get(f"{url}/{symbol}?apikey={key}")
    for dictionary in response.json():
        if dictionary['symbol'] == GOLD_COMM_SYMBOL:
            return dictionary
    raise Exception("Quote not found in response")


def get_gold_price():
    quote = get_fmp_quote(GOLD_COMM_SYMBOL)
    return quote['price']


def is_symbol_in_iex_universe(symbol):
    for entry in get_iex_symbol_universe():
        if symbol == entry['symbol']:
            return True
    return False


def commaify(data):
    if data is None:
        return data
    return "{:,}".format(data)


class QuoteCommand(PluginBase):

    command = "quote"
    usage = "quote $symbol"
    description = "Quote including data beyond price."

    def __init__(self):
        pass

    @staticmethod
    def _build_gold_quote_msg_block(quote):
        blocks = []

        symbol = quote.get("symbol")
        name = quote.get("name")
        price = commaify(quote.get("price"))
        high52 = commaify(quote.get("yearHigh"))
        low52 = commaify(quote.get("yearLow"))
        avg50 = commaify(quote.get("priceAvg50"))
        avg200 = commaify(quote.get("priceAvg200"))
        volume = commaify(quote.get("volume"))
        avg_volume = commaify(quote.get("avgVolume"))
        prev_close = commaify(quote.get("previousClose"))

        blocks.append(
                HeaderBlock(
                    text=f"{symbol} - {name}"))
        blocks.append(DividerBlock)

        blocks.append(
                SectionBlock(
                    text=f"*Price:* {price} *--* *Prev. Close:* {prev_close}"))
        blocks.append(DividerBlock)

        blocks.append(
                SectionBlock(
                    text=(f"*Volume:* {volume} *--* "
                          f"*Avg Volume:* {avg_volume}")))
        blocks.append(DividerBlock)

        blocks.append(
                SectionBlock(
                    text=((f"*52 High:* {high52} *--* "
                           f"*52w Low:* {low52} *--* "))))
        blocks.append(DividerBlock)

        blocks.append(
            SectionBlock(
                text=f"*50 MA:* {avg50} *--* *200 MA:* {avg200}"))
        blocks.append(DividerBlock)

    @staticmethod
    def _build_quote_msg_block(quote):
        blocks = []

        symbol = quote.get("symbol")
        name = quote.get("companyName")
        price = quote.get("latestPrice")
        market_cap = commaify(quote.get("marketCap"))
        volume = commaify(quote.get("volume"))
        avg_volume = commaify(quote.get("avgTotalVolume"))
        pe = commaify(quote.get("peRatio"))
        high52 = commaify(quote.get("week52High"))
        low52 = commaify(quote.get("week52Low"))
        ytd = "{:.0%}".format(quote.get("ytdChange"))

        blocks.append(HeaderBlock(
            text=f"{symbol} - {name}"))
        blocks.append(DividerBlock())

        blocks.append(
                SectionBlock(
                    text=f"*Price:* {price} *--* *P/E:* {pe}"))
        blocks.append(DividerBlock())

        blocks.append(
                SectionBlock(
                    text=(f"*Market cap:* {market_cap} *--* "
                          f"*Volume:* {volume} *--* *Avg*: {avg_volume}")))
        blocks.append(DividerBlock())

        blocks.append(SectionBlock(
            text=(f"*52 High:* {high52} *--* *52w Low:* {low52} *--* "
                  f"*Ytd:* {ytd}")))

        return blocks

    def _get_gold_quote_blocks(self, symbol):
        quote = get_fmp_quote(symbol)
        blocks = self._build_gold_quote_msg_block(quote)
        return blocks

    def _get_stock_quote_blocks(self, symbol):
        quote = Stock(symbol).get_quote()
        blocks = self._build_quote_msg_block(quote)
        return blocks

    def run(self, *args, **kwargs):
        args = list(args)
        symbol = args.pop(0)
        symbol_err = SectionBlock(text=f"Symbol `{symbol}` not found")

        if symbol in GOLD_ALIASES:
            blocks = self._get_gold_quote_blocks(GOLD_COMM_SYMBOL)
            return blocks

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
        if symbol in GOLD_ALIASES:
            symbol = GOLD_COMM_SYMBOL
            price = get_gold_price()
            return SectionBlock(text=f"`{symbol}` `{price}`")

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
