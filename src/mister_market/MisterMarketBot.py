import logging
from . import chart_commands, stock_commands # noqa ignore=F405
from .plugin_base import PluginBase
from .SymbolResolver import SymbolResolver
from .slack import BlockBuilder, MessageBuilder

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class MisterMarketBot:

    plugins = []

    def __init__(self):
        self.plugins = PluginBase().subclasses
        if not len(set(self.plugins)) == len(self.plugins):
            raise Exception("Plugin command collision")
        logger.debug(f"Initialized plugins: {self.plugins}")
        self.symbolResolver = SymbolResolver()

    def _parse_command(self, command_string):
        command_list = command_string.split()
        command = command_list.pop(0)
        return command, command_list

    def _is_command(self, command):
        return any([command == p.command for p in self.plugins])

    def _get_plugin(self, command):
        for plugin in self.plugins:
            if command == plugin.command:
                return plugin()
        return None

    def handle_slack_message(self, message):
        logging.debug(f"received message: {message}")
        tokenized_message = message.split()
        # _userid = tokenized_message[0]
        maybe_command = tokenized_message[1]
        if maybe_command.lower() == "help":
            message_builder = MessageBuilder()
            block_builder = BlockBuilder()
            message_builder.add_text("`price $symbol` Get just the price. ")
            message_builder.add_text("Example: @mistermarket price AAPL\n")

            message_builder.add_text("`quote $symbol` Get a more detailed quote. ")
            message_builder.add_text("Example: @mistermarket quote AAPL \n")

            message_builder.add_text("`indexes` Get quotes on major indexes. ")
            message_builder.add_text("Example: @mistermarket indexes \n")
            message_builder.add_text("`help` This message. \n")
            message_builder.add_text("BETA: `$company` Find a quote for $company. ")
            message_builder.add_text("Example: @mistermarket Apple \n")
            block_builder.add_section_block(message_builder.product)
            return block_builder.product

        if self._is_command(maybe_command):
            args = tokenized_message[2:]
            logging.debug(f"Running command: {maybe_command} with args: {args}")
            return self._get_plugin(maybe_command).run(*args)

        # If we don't identify the second token as a command
        # then pass the entire message minus the username
        # into the fuzzy resolver.
        message_string_sans_username = " ".join(tokenized_message[1:])
        logging.debug(f"Attempting fuzzy lookup of {message_string_sans_username}")
        maybe_symbol = self.symbolResolver.fuzzy_symbol_lookup(message_string_sans_username)

        if maybe_symbol is not None:
            logging.debug(f"Resolved fuzzy lookup to symbol: {maybe_symbol}")
            return self._get_plugin("quote").run(maybe_symbol)

        message_builder = MessageBuilder()
        block_builder = BlockBuilder()
        message_builder.add_text("I don't understand your command:")
        message_builder.add_terminal_text(maybe_command)
        block_builder.add_section_block(message_builder.product)
        return block_builder.product
