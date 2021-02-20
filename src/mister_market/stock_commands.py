import dateutil
from iexfinance import altdata
from iexfinance.stocks import Stock
from iexfinance.utils.exceptions import IEXQueryError
from prettytable import PrettyTable
from . import helpers
from .constants import MisterMarketConstants
from .plugin_base import PluginBase
from .slack import BlockBuilder, MessageBuilder
from mister_market.quotes import FmpQuote
from mister_market.pretty_tables import QuotePrettyTable

UP_ARROW = ":arrow_upper_right:"
DOWN_ARROW = ":arrow_lower_right:"
FLAT_ARROW = ":left_right_arrow:"
constants = MisterMarketConstants()


class ExpirationCommand(PluginBase):
    command = "expiration"
    usage = "expiration $symbol"
    description = "get options expiration dates for $symbol"

    def __init__(self):
        pass

    def run(self, *args, **kwargs):
        args = list(args)
        symbol = args.pop(0)
        symbol = symbol.upper()
        expirations = helpers.get_options_expiration(symbol)
        pt = PrettyTable()
        pt.align = 'l'
        pt.field_names = ['{} Option Expirations'.format(symbol)]
        pt.sortby = '{} Option Expirations'.format(symbol)
        for expiration in expirations:
            pt.add_row([expiration])
        block_builder = BlockBuilder()
        message_builder = MessageBuilder()
        message_builder.add_text(f'```{pt.get_string()}```')
        block_builder.add_section_block(message_builder.product)
        return block_builder.product


class ChainsCommand(PluginBase):
    command = "chain"
    usage = "chain $symbol $expiration $strike"
    description = "get options expiration dates for $symbol"

    def __init__(self):
        pass

    def run(self, *args, **kwargs):
        block_builder = BlockBuilder()
        args_len = len(args)
        if args_len < 3:
            block_builder.add_section_block(("Invalid arguments. "
                                             "Try $symbol $expiration $strike $call/$put"))
            return block_builder.product
        args = list(args)
        symbol = args.pop(0).upper()
        expiration = args.pop(0)
        strike = args.pop(0)
        option_type = None
        if args_len > 3:
            option_type = args.pop(0)
            if option_type.lower() not in ["put", "puts", "call", "calls"]:
                block_builder.add_section_block(("Invalid arguments. "
                                                 "Try $symbol $expiration $strike $call/$put"))
                return block_builder.product

        try:
            float(strike)
            dateutil.parser.parse(expiration)
        except ValueError:
            block_builder.add_section_block(("Invalid arguments. "
                                             "Try $symbol $expiration $strike $call/$put"))
            return block_builder.product

        expirations = helpers.get_options_expiration(symbol)
        if expiration not in expirations:
            block_builder.add_section_block(
                "Invalid expiration. Try one of these {}".format(expirations))
            return block_builder.product
        chains = helpers.get_options_chains_near_strike_tabulated(symbol, expiration, strike)
        message_builder = MessageBuilder()
        if option_type is None or option_type in ["call", "calls"]:
            message_builder.add_bold_text(f"{symbol} Calls")
            message_builder.add_text(f'```{chains["calls"]}```')
            block_builder.add_section_block(message_builder.product)
        if option_type is None or option_type in ["put", "puts"]:
            message_builder.add_bold_text(f"{symbol} Puts")
            message_builder.add_text(f'```{chains["puts"]}```')
            block_builder.add_section_block(message_builder.product)
        return block_builder.product


class NewsCommand(PluginBase):
    command = "news"
    usage = "news $symbol"
    description = "get news for a symbol"

    def __init__(self):
        pass

    def run(self, *args, **kwargs):
        args = list(args)
        symbol = args.pop(0)
        symbol = symbol.upper()
        news = helpers.get_iex_symbol_news(symbol)
        block_builder = BlockBuilder()
        message_builder = MessageBuilder()
        for article in news:
            if article.get("lang") != "en":
                continue

            message_builder.add_bold_text(article.get("headline"))
            message_builder.add_text("source: {}".format(article.get("source")))
            message_builder.add_text(article.get("url"))
            block_builder.add_section_block(message_builder.product)
        return block_builder.product


class IndexesCommand(PluginBase):
    command = "indexes"
    usage = "indexes or indexes all"
    description = "Get index changes."

    def __init__(self):
        pass

    @staticmethod
    def _build_index_msg_block(data):
        block_builder = BlockBuilder()
        message_builder = MessageBuilder()
        pt = PrettyTable()
        pt.align = 'l'
        pt.field_names = ['Index', 'Gainz', 'Price', 'Open', 'Prev Close',
                          'Day High', 'Day Low']
        pt.sortby = "Gainz"
        for index in data:
            pt.add_row([index.get("symbol"),
                        "{}%".format(
                            index.get("changesPercentage")),
                        helpers.commaify(index.get("price")),
                        helpers.commaify(index.get("open")),
                        helpers.commaify(index.get("previousClose")),
                        helpers.commaify(index.get("dayHigh")),
                        helpers.commaify(index.get("dayLow"))])

        message_builder.add_text("```{}```".format(
            pt.get_string(title="Indexes")))
        block_builder.add_section_block(message_builder.product)

        return block_builder.product

    def _get_index_blocks(self):
        data = helpers.get_fmp_indexes(brief=True)
        blocks = self._build_index_msg_block(data)
        return blocks

    def run(self, *args, **kwargs):
        return self._get_index_blocks()


class QuoteCommand(PluginBase):
    command = "quote"
    usage = "quote $symbol"
    description = "Quote including data beyond price."

    def __init__(self):
        pass

    @staticmethod
    def _build_quote_msg_block(symbol):
        quote = FmpQuote(symbol)
        text_table = QuotePrettyTable(quote).build_table()
        block_builder = BlockBuilder()
        message_builder = MessageBuilder()
        message_builder.add_text("```{}```".format(
            text_table))
        block_builder.add_section_block(message_builder.product)
        chart_url = f"https://mistermarket.io/stocks/{symbol}/chart"
        img_url = f"https://mistermarket.io/stocks/{symbol}/chart.png"
        block_builder.add_image_block(img_url, symbol)
        block_builder.add_section_block(chart_url)
        return block_builder.product

    def run(self, *args, **kwargs):
        args = list(args)
        symbol = args.pop(0)
        symbol = symbol.upper()

        message_builder = MessageBuilder()
        message_builder.add_text("Symbol")
        message_builder.add_terminal_text(symbol)
        message_builder.add_text("not found.")
        block_builder = BlockBuilder()
        block_builder.add_section_block(text=message_builder.product)
        error = block_builder.product

        if symbol in helpers.get_fmp_symbol_universe():
            return self._build_quote_msg_block(symbol)

        return error


class PriceCommand(PluginBase):
    command = "price"
    usage = "price $symbol"
    description = "Retrieve a price for a supported symbol."

    def __init__(self):
        pass

    @staticmethod
    def _get_stock_price(symbol):
        return Stock(symbol, output_format='json').get_price()

    @staticmethod
    def _get_crypto_price(symbol):
        if symbol.lower() == "btc":
            symbol = "BTCUSD"
        quote = altdata.get_crypto_quote(symbol, output_format='json')
        price = quote['latestPrice']
        return price

    def run(self, *args, **kwargs):
        args = list(args)
        symbol = args.pop(0)
        symbol = symbol.upper()

        # Error message blocks
        message_builder = MessageBuilder()
        message_builder.add_text("Symbol")
        message_builder.add_terminal_text(symbol)
        message_builder.add_text("not found.")
        block_builder = BlockBuilder()
        block_builder.add_section_block(text=message_builder.product)
        error = block_builder.product

        if symbol in constants.GOLD_SYMBOL_ALIASES:
            symbol = constants.FMP_GOLD_SYMBOL
            price = helpers.get_gold_price()
            message_builder.add_terminal_text(symbol)
            message_builder.add_terminal_text(price)
            block_builder.add_section_block(message_builder.product)
            return block_builder.product

        if helpers.is_symbol_in_iex_universe(symbol):
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
