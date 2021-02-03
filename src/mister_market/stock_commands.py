from iexfinance import altdata
from iexfinance.stocks import Stock
from iexfinance.utils.exceptions import IEXQueryError
from prettytable import PrettyTable
from . import helpers
from .constants import MisterMarketConstants
from .plugin_base import PluginBase
from .slack import BlockBuilder, MessageBuilder

UP_ARROW = ":arrow_upper_right:"
DOWN_ARROW = ":arrow_lower_right:"
FLAT_ARROW = ":left_right_arrow:"
constants = MisterMarketConstants()


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
        for article in news[symbol]["news"]:
            if article.get("lang") != "en":
                continue
            if article.get("image") is not None:
                block_builder.add_image_block(article.get("image"),
                                              article.get("source"))

            message_builder.add_text(article.get("headline"))
            message_builder.add_text(article.get("source"))
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
    def _build_gold_quote_msg_block(quote):
        pt = PrettyTable()
        pt.align = 'l'
        pt.field_names = ['Gainz', 'Price', 'Open', 'Prev Close',
                          'Day High', 'Day Low']
        pt.add_row(["{}%".format(
            quote.get("changesPercentage")),
            helpers.commaify(quote.get("price")),
            helpers.commaify(quote.get("open")),
            helpers.commaify(quote.get("previousClose")),
            helpers.commaify(quote.get("dayHigh")),
            helpers.commaify(quote.get("dayLow"))])

        block_builder = BlockBuilder()
        message_builder = MessageBuilder()

        message_builder.add_text("```{}```".format(
            pt.get_string(title=quote.get("symbol"))))
        block_builder.add_section_block(message_builder.product)
        gold_chart = "https://goldprice.org/charts/history/gold_1_year_o_usd_x.png"
        block_builder.add_image_block(gold_chart, "Gold Chart")
        block_builder.add_section_block("https://goldprice.org/spot-gold.html")

        return block_builder.product

    @staticmethod
    def _build_quote_msg_block(quote):
        pt = PrettyTable()
        pt.align = 'l'
        pt.field_names = ['Gainz', 'Price', 'Open', 'Prev Close',
                          'Day High', 'Day Low', '52 H', '52 L', '200 MA']
        pt.add_row(["{}%".format(quote.get("changesPercentage")),
                    helpers.commaify(quote.get("price")),
                    helpers.commaify(quote.get("open")),
                    helpers.commaify(quote.get("previousClose")),
                    helpers.commaify(quote.get("dayHigh")),
                    helpers.commaify(quote.get("dayLow")),
                    helpers.commaify(quote.get("yearHigh")),
                    helpers.commaify(quote.get("yearLow")),
                    "%.2f" % quote.get("priceAvg200")])

        block_builder = BlockBuilder()
        message_builder = MessageBuilder()

        symbol = quote.get("symbol")
        message_builder.add_text("```{}```".format(
            pt.get_string(title=symbol)))
        block_builder.add_section_block(message_builder.product)
        chart = f"https://finviz.com/chart.ashx?t={symbol}&ty=c&ta=1&p=d&s=l"
        block_builder.add_image_block(chart, symbol)
        block_builder.add_section_block(chart)
        return block_builder.product

    def _get_gold_quote_blocks(self, symbol):
        quote = helpers.get_fmp_quote(symbol)
        blocks = self._build_gold_quote_msg_block(quote)
        return blocks

    def _get_stock_quote_blocks(self, symbol):
        quote = helpers.get_fmp_quote(symbol)
        # quote = Stock(symbol, output_format='json').get_quote()
        blocks = self._build_quote_msg_block(quote)
        return blocks

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

        if symbol in constants.GOLD_SYMBOL_ALIASES:
            return self._get_gold_quote_blocks(
                constants.FMP_GOLD_SYMBOL)

        if helpers.is_symbol_in_iex_universe(symbol):
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
