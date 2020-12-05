from slackblocks import DividerBlock, HeaderBlock, SectionBlock


class MessageBuilder(object):

    def __init__(self):
        self.message = []

    @property
    def product(self):
        return ' '.join(self.message)

    def reset(self):
        self.message = []

    def add_text(self, text):
        self.message.append(text)

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
        return self.blocks

    def reset(self):
        self.blocks = []

    def add_divider_block(self):
        self.blocks.append(DividerBlock())

    def add_header_block(self, text):
        self.blocks.append(HeaderBlock(text=text))

    def add_section_block(self, text):
        self.blocks.append(SectionBlock(text=text))
