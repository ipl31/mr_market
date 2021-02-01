from slackblocks import (DividerBlock,
                         HeaderBlock,
                         ImageBlock,
                         SectionBlock)


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

    def add_section_block(self, text):
        self.blocks.append(SectionBlock(text=text))
