import logging
import pprint
from .helpers import get_public_methods
from .ISkill import ISkill
from iexfinance.stocks import Stock


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

HELP_COMMAND = "help"
IEX_STOCK_SKILL_ID = "stock"


class IexStockSkill(ISkill):

    def __init__(self):
        pass

    def _get_commands(self):
        commands = get_public_methods(Stock)
        commands.append(HELP_COMMAND)
        return commands

    @property
    def skill_id(self):
        return IEX_STOCK_SKILL_ID

    def execute(self, command, *args):
        msg = f"received command: {command} args:{args}"
        logger.debug(msg)
        if command == HELP_COMMAND:
            commands = []
            commands = [f"`{cmd}`" for cmd in self._get_commands()]
            return ' '.join(commands)
        if command not in self._get_commands():
            msg = f"I don't know the command: `{command}`"
            return msg
        args_list = list(*args)
        logger.debug(f"args list {args_list}")
        stock = Stock(args_list.pop(0))
        logger.debug(f"symbol {stock.symbols}")
        results = getattr(stock, command)(*args_list)
        return "`{}`".format(pprint.pformat(results))

    def get_help(self):
        return self._get_commands()

    def get_commands(self):
        return self._get_commands()
