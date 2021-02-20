from . import helpers
from .constants import MisterMarketConstants
from fuzzywuzzy import process
constants = MisterMarketConstants()


class SymbolResolver(object):
    """ Class to provide lookup/resolution of symbols"""

    def __init__(self):
        self.fmp_stocks = helpers.get_fmp_stock_universe()
        self.fmp_stock_symbols = [d["symbol"] for d in self.fmp_stocks]
        self.fmp_cryptos = helpers.get_fmp_crypto_symbol_universe()
        self.fmp_crypto_symbols = [d["symbol"] for d in self.fmp_cryptos]
        self.fmp_commodities = helpers.get_fmp_commodity_symbol_universe()
        self.fmp_commodities_symbols = [d["symbol"] for d in self.fmp_commodities]
        self.fmp_forex = helpers.get_fmp_fx_symbol_universe()
        self.fmp_forex_symbols = [d["ticker"] for d in self.fmp_forex]

    def symbol_resolve(self, symbol):
        symbol = symbol.upper()
        if symbol in self.fmp_stock_symbols:
            return symbol, constants.DATA_SOURCE_FMP, constants.STOCK
        if symbol in self.fmp_crypto_symbols:
            return symbol, constants.DATA_SOURCE_FMP, constants.CRYPTO
        if symbol in self.fmp_forex_symbols:
            return symbol, constants.DATA_SOURCE_FMP, constants.FOREX
        if symbol in self.fmp_commodities_symbols:
            return symbol, constants.DATA_SOURCE_FMP, constants.COMMODITY
        return None

    def fuzzy_symbol_lookup(self, string):
        """ Given a string try to find an suitable ticker. Expected strings are things such as
        company name and commodity name."""
        fx_result = process.extractOne(string, self.fmp_forex)
        crypto_result = process.extractOne(string, self.fmp_cryptos)
        commodities_result = process.extractOne(string, self.fmp_commodities)
        stock_results = process.extractOne(string, self.fmp_stocks)
        matches = sorted([fx_result, crypto_result, commodities_result, stock_results],
                         reverse=True,
                         key=lambda x: x[1])
        best_match = matches[0]
        if best_match[1] < 60:
            return None
        return matches[0][0]['symbol']
