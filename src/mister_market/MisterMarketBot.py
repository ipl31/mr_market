from . import stock_commands
from .plugin_base import PluginBase


class MisterMarketBot:

    plugins = []

    def __init__(self):
        self.plugins = PluginBase().subclasses
        if not len(set(self.plugins)) == len(self.plugins):
            raise Exception("Plugin command collision")

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
        command, args = self._parse_command(message)
        if not self._is_command(command):
            return f"I do not understand your command: `{command}`"
        return self._get_plugin(command).run(*args)
