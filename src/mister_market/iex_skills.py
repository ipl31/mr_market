"""
Classes to provide bot skills for IEX API calls.
"""
import logging
import pprint
from iexfinance.stocks import Stock
from iexfinance.utils.exceptions import IEXQueryError
from .helpers import get_public_methods
from .ISkill import ISkill

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

HELP_COMMAND = "help"
IEX_STOCK_SKILL_ID = "stock"


class IexStockSkill(ISkill):
    """ IexStockSkill is an ISkill impl that provides the ability
    to execute commands on instances of the Stock class from
    the iex_finance module. It does this by providing a way to map
    method names on Stock() to command strings.
    """

    @staticmethod
    def _get_commands():
        commands = get_public_methods(Stock)
        commands.append(HELP_COMMAND)
        return commands

    @property
    def skill_id(self):
        return IEX_STOCK_SKILL_ID

    def _execute(self, command, *args):
        msg = "received command: %s args:%s"
        logger.debug(msg, command, args)
        if command == HELP_COMMAND:
            commands = []
            commands = [f"`{cmd}`" for cmd in self._get_commands()]
            return ' '.join(commands)
        if command not in self._get_commands():
            msg = f"I don't know the command: `{command}`"
            return msg
        args_list = list(*args)
        logger.debug("args list: %s", args_list)
        stock = Stock(args_list.pop(0))
        logger.debug("symbol %s", stock.symbols)
        method = getattr(stock, command)
        result = method(*args_list)
        return "`{}`".format(pprint.pformat(result))

    def execute(self, command, *args):
        try:
            result = self._execute(command, *args)
            return result
        except IEXQueryError:
            logger.exception("IEX query failed %s %s",
                             command, args)
            msg = f"IEX error, check symbol is valid: {args}"
            return msg

    def get_help(self):
        return self._get_commands()

    def get_commands(self):
        return self._get_commands()
