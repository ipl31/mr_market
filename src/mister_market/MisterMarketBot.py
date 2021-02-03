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
        # Strip user id from message:
        message = message.split(' ', 1)[1]
        logging.debug(f"bot message: {message}")
        command, args = self._parse_command(message)
        if self._is_command(command):
            return self._get_plugin(command).run(*args)
        # If we don't identify the first token as a command
        # then pass the entire message into the fuzzy resolver.
        maybe_symbol = self.symbolResolver.fuzzy_symbol_lookup(message)
        if maybe_symbol is not None:
            return self._get_plugin("quote").run(*args)

        message_builder = MessageBuilder()
        block_builder = BlockBuilder()
        message_builder.add_text("I don't understand your command:")
        message_builder.add_terminal_text(command)
        block_builder.add_section_block(message_builder.product)
        return block_builder.product
