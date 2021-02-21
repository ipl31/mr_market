from slackblocks import (DividerBlock,
                         HeaderBlock,
                         ImageBlock,
                         SectionBlock)
from slackblocks.elements import Text
from mister_market.helpers import commaify, millify


class MessageBuilder(object):

    def __init__(self):
        self.message = []

    @property
    def product(self):
        product = ' '.join(self.message)
        self.reset()
        return product

    def reset(self):
        self.message = []

    def add_text(self, text):
        self.message.append(text)

    def add_link(self, text):
        self.message.append(f"<{text}>")

    def add_bold_text(self, text):
        self.message.append(f"*{text}*")

    def add_terminal_text(self, text):
        self.message.append(f"`{text}`")

    def add_multiline_terminal_text(self, text):
        self.message.append(f"```{text}```")


class BlockBuilder(object):

    def __init__(self):
        self.blocks = []

    @property
    def product(self):
        product = self.blocks
        self.reset()
        return product

    def reset(self):
        self.blocks = []

    def add_image_block(self, url, alt_text, title=None):
        self.blocks.append(ImageBlock(url, alt_text, title))

    def add_divider_block(self):
        self.blocks.append(DividerBlock())

    def add_header_block(self, text):
        self.blocks.append(HeaderBlock(text=text))

    def add_section_block(self, text=None, fields=None):
        self.blocks.append(SectionBlock(text=text, fields=fields))


class QuoteBlock:

    def __init__(self, quote):
        self.quote = quote
        self.block_builder = BlockBuilder()

    def build_quote(self):
        self.block_builder.add_header_block(self.quote.name)
        self.block_builder.add_image_block(self.quote.chart_image_url,
                                           alt_text=f"{self.quote.symbol} Chart")
        if self.quote.price is not None:
            self.quote.price = commaify(self.quote.price)
        fields = [Text(f"*Price:* ${self.quote.price}")]

        arrow = ""
        if isinstance(self.quote.change_value, float) or isinstance(self.quote.change_value, int):
            if self.quote.change_value == 0:
                arrow = ":zero:"
            elif self.quote.change_value < 0:
                arrow = ":arrow_down:"
            else:
                arrow = ":arrow_up:"

        if self.quote.change_value is not None:
            self.quote.change_value = commaify(self.quote.change_value)
        if self.quote.open is not None:
            self.quote.open = commaify(self.quote.open)
        if self.quote.volume_avg is not None:
            self.quote.volume_avg = millify(self.quote.volume_avg)
        if self.quote.volume_day is not None:
            self.quote.volume_day = millify(self.quote.volume_day)
        if self.quote.previous_close is not None:
            self.quote.previous_close = commaify(self.quote.previous_close)
        if self.quote.high_day is not None:
            self.quote.high_day = commaify(self.quote.high_day)
        if self.quote.low_day is not None:
            self.quote.low_day = commaify(self.quote.low_day)
        if self.quote.market_cap is not None:
            self.quote.market_cap = millify(self.quote.market_cap)
        if self.quote.high_52w is not None:
            self.quote.high_52w = commaify(self.quote.high_52w)
        if self.quote.low_52w is not None:
            self.quote.low_52w = commaify(self.quote.low_52w)

        fields.append(Text(
            f"*Change:* {arrow} ${self.quote.change_value} {self.quote.change_percentage}%"))
        fields.append(Text(f"*Open:* ${self.quote.open}"))
        fields.append(Text(f"*Volume/Avg:* {self.quote.volume_day}/{self.quote.volume_avg}"))
        fields.append(Text(f"*Prev Close:* ${self.quote.previous_close}"))
        fields.append(Text(f"*Day High/Low:* ${self.quote.high_day}/${self.quote.low_day}"))
        fields.append(Text(f"*Market Cap:* {self.quote.market_cap}"))
        fields.append(Text(f"*52w High/Low:* ${self.quote.high_52w}/${self.quote.low_52w}"))
        fields.append(Text(f"*P/E Ratio:* {self.quote.pe_ratio}"))
        self.block_builder.add_section_block(text=self.quote.chart_url,
                                             fields=fields)
        return self.block_builder.product
