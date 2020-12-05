import os
import requests
from functools import lru_cache
from iexfinance import altdata, refdata
from iexfinance.stocks import Stock
from iexfinance.utils.exceptions import IEXQueryError
from slackblocks import HeaderBlock, DividerBlock, SectionBlock
from .plugin_base import PluginBase
from .slack import BlockBuilder, MessageBuilder

GOLD_ALIASES = ["GCUSD", "XAUUSD", "XAU"]
GOLD_COMM_SYMBOL = "GCUSD"


@lru_cache(maxsize=1)
def get_iex_symbol_universe():
    return refdata.get_symbols()


def get_fmp_quote(symbol):
    key = os.environ["FMP_API_KEY"]
    url = "https://financialmodelingprep.com/api/v3/quote"
    response = requests.get(f"{url}/{symbol}?apikey={key}")
    for dictionary in response.json():
        if dictionary['symbol'] == GOLD_COMM_SYMBOL:
            return dictionary
    raise Exception(f"Quote for {symbol} not found in response")


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

        block_builder = BlockBuilder()
        message_builder = MessageBuilder()

        message_builder.add_text(symbol)
        message_builder.add_text("--")
        message_builder.add_text(name)
        block_builder.add_header_block(message_builder.product)
        block_builder.add_divider_block()

        message_builder.add_bold_text("Price:")
        message_builder.add_text(price)
        message_builder.add_bold_text("--")
        message_builder.add_bold_text("Prev Close")
        message_builder.add_text(prev_close)
        block_builder.add_section_block(message_builder.product)
        block_builder.add_divider_block()

        message_builder.add_bold_text("Volume:")
        message_builder.add_text(volume)
        message_builder.add_bold_text("--")
        message_builder.add_bold_text("Avg Volume")
        message_builder.add_text(avg_volume)
        block_builder.add_section_block(message_builder.product)
        block_builder.add_divider_block()

        message_builder.add_bold_text("52 High")
        message_builder.add_text(high52)
        message_builder.add_bold_text("--")
        message_builder.add_bold_text("52 Low")
        message_builder.add_text(low52)
        block_builder.add_section_block(message_builder.product)
        block_builder.add_divider_block()

        message_builder.add_bold_text("50 MA:")
        message_builder.add_text(avg50)
        message_builder.add_bold_text("--")
        message_builder.add_bold_text("200 MA:")
        message_builder.add_text(avg200)
        block_builder.add_section_block(message_builder.product)

        return block_builder.product

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

        message_builder = MessageBuilder()
        message_builder.add_text("Symbol")
        message_builder.add_terminal_text(symbol)
        message_builder.add_text("not found.")
        block_builder = BlockBuilder()
        block_builder.add_section_block(text=message_builder.product)
        error = block_builder.product

        if symbol.lower() in [x.lower() for x in GOLD_ALIASES]:
            return self._get_gold_quote_blocks(GOLD_COMM_SYMBOL)

        if is_symbol_in_iex_universe(symbol):
            return self._get_stock_quote_blocks(symbol)

        return error


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

        # Error message blocks
        message_builder = MessageBuilder()
        message_builder.add_text("Symbol")
        message_builder.add_terminal_text(symbol)
        message_builder.add_text("not found.")
        block_builder = BlockBuilder()
        block_builder.add_section_block(text=message_builder.product)
        error = block_builder.product

        if symbol.lower() in [x.lower() for x in GOLD_ALIASES]:
            symbol = GOLD_COMM_SYMBOL
            price = get_gold_price()
            message_builder.add_terminal_text(symbol)
            message_builder.add_terminal_text(price)
            block_builder.add_section_block(message_builder.product)
            return block_builder.product

        if is_symbol_in_iex_universe(symbol):
            price = self._get_stock_price(symbol)
            message_builder.add_terminal_text(symbol)
            message_builder.add_terminal_text(price)
            block_builder.add_section_block(message_builder.product)
            return block_builder.product

        try:
            price = self._get_crypto_price(symbol)
            if price is None:
                return error
            message_builder.add_terminal_text(symbol)
            message_builder.add_terminal_text(price)
            block_builder.add_section_block(message_builder.product)
            return block_builder.product

        except IEXQueryError:
            return error
