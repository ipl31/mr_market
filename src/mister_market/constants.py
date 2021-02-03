
class ConstantError(Exception):
    def __init__(self, message="Can't redfine constants"):
        self.message = message
        super().__init__(self.message)


def constant(f):

    def fset(self, value):
        raise ConstantError

    def fget(self):
        return f()
    return property(fget, fset)


class MisterMarketConstants(object):

    def __init__(self):
        pass

    @constant
    def DATA_SOURCE_IEX():
        return "IEX"

    @constant
    def DATA_SOURCE_FMP():
        return "Financial Modeling Prep"

    @constant
    def FMP_GOLD_SYMBOL():
        return "GCUSD"

    @constant
    def GOLD_SYMBOL_ALIASES():
        return ["GCUSD", "XAUUSD", "XAU"]

    @constant
    def STOCK():
        return "stock"

    @constant
    def COMMODITY():
        return "commodity"

    @constant
    def CRYPTO():
        return "crypto"

    @constant
    def FOREX():
        return "forex"
