import pprint
from .helpers import get_public_methods
from .ISkill import ISkill
from iexfinance.stocks import Stock


class IexStockSkill(ISkill):

    def __init__(self):
        pass

    def _get_commands(self):
        return get_public_methods(Stock)

    @property
    def skill_id(self):
        return "stock"

    def execute(self, command, *args):
        args_list = list(*args)
        stock = Stock(args_list.pop()[0])
        if command == "help":
            return self._get_commands()
        if command not in self._get_commands():
            return "error"
        results = getattr(stock, command)(*args_list)
        return pprint.pformat(results)

    def get_help(self):
        return self._get_commands()

    def get_commands(self):
        return self._get_commands()
