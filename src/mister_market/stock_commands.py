from iexfinance import altdata
from iexfinance.stocks import Stock
from iexfinance.utils.exceptions import IEXQueryError
from slackblocks import HeaderBlock, DividerBlock, SectionBlock
from . import constants, helpers
from .plugin_base import PluginBase
from .slack import BlockBuilder, MessageBuilder


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

        for index in data:
            # symbol = index.get("symbol")
            name = index.get("name")
            price = helpers.commaify(index.get("price"))
            day_high = helpers.commaify(index.get("dayHigh"))
            day_low = helpers.commaify(index.get("dayLow"))
            change = helpers.commaify(index.get("changesPercentage"))
            # year_high = data.get("yearHigh")
            # year_low = data.get("yearLow")
            # price_avg_50 = data.get("priceAvg50")
            price_avg_200 = index.get("priceAvg200")
            # volume = data.get("volume")
            # avg_volume = data.get("avgVolume")
            # open_price = data.get("open")
            previous_close = helpers.commaify(index.get("previousClose"))

            # Table headers
            header_name = "| {:<30}".format("Index"[:30])
            header_price = "| {:<20}".format("Price"[:20])
            header_gains = "| {:<10}".format("Gainz"[:10])
            day_high_low = "| {:<30}".format("Day H/L"[:20])
            avg_200 = "| {:<20}".format("200 MA"[:10])

            message_builder.add_bold_text(''.join([header_name,
                                                  header_price,
                                                  header_gains,
                                                  day_high_low,
                                                  avg_200]))
            block_builder.add_section_block(message_builder.product)

            if price > previous_close:
                arrow = ":arrow_upper_right:"
            if price < previous_close:
                arrow = ":arrow_lower_right:"
            message_builder.add_bold_text("| {:<30}".format(name[:30]))
            message_builder.add_text("| {:<20}".format(price[:20]))
            gains = "| {} {}".format(change, arrow)
            message_builder.add_text("| {:<10}".format(gains))
            high_low = "| {} / {}".format(day_high, day_low)
            message_builder.add_text("{:<30}".format(high_low))
            message_builder.add_text("{:<20}".format(price_avg_200))

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
        symbol = quote.get("symbol")
        name = quote.get("name")
        price = helpers.commaify(quote.get("price"))
        high52 = helpers.commaify(quote.get("yearHigh"))
        low52 = helpers.commaify(quote.get("yearLow"))
        avg50 = helpers.commaify(quote.get("priceAvg50"))
        avg200 = helpers.commaify(quote.get("priceAvg200"))
        volume = helpers.commaify(quote.get("volume"))
        avg_volume = helpers.commaify(quote.get("avgVolume"))
        prev_close = helpers.commaify(quote.get("previousClose"))

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
        market_cap = helpers.commaify(quote.get("marketCap"))
        volume = helpers.commaify(quote.get("volume"))
        avg_volume = helpers.commaify(quote.get("avgTotalVolume"))
        pe = helpers.commaify(quote.get("peRatio"))
        high52 = helpers.commaify(quote.get("week52High"))
        low52 = helpers.commaify(quote.get("week52Low"))
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
        quote = helpers.get_fmp_quote(symbol)
        blocks = self._build_gold_quote_msg_block(quote)
        return blocks

    def _get_stock_quote_blocks(self, symbol):
        quote = Stock(symbol, output_format='json').get_quote()
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

        if symbol in constants.GOLD_ALIASES:
            return self._get_gold_quote_blocks(constants.GOLD_COMM_SYMBOL)

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

        if symbol in constants.GOLD_ALIASES:
            symbol = constants.GOLD_COMM_SYMBOL
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
