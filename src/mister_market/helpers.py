import os
import requests
from .constants import MisterMarketConstants
from functools import lru_cache
from iexfinance import refdata
from iexfinance.stocks import Stock

FMP_API_KEY = os.environ["FMP_API_KEY"]
constants = MisterMarketConstants()


def commaify(data):
    if data is None:
        return data
    return "{:,}".format(data)


@lru_cache(maxsize=1)
def get_iex_symbol_universe():
    return refdata.get_symbols(output_format='json')


def get_iex_symbol_news(symbol, limit=5):
    stock = Stock(symbol)
    return stock.get_news(last=limit)


def get_fmp_indexes(brief=True):
    indexes_brief = ["^GSPC",
                     "^IXIC",
                     "^RUT",
                     "^VIX",
                     "DX-Y.NYB",
                     "^GVZ",
                     "^FTSE",
                     "^KS11",
                     "^GDAXI",
                     "^N225",
                     "IMOEX.ME",
                     "^OVX"
                     "^NSEI",
                     "^DJT",
                     "^DJI",
                     "^SSEC"]

    url = "https://financialmodelingprep.com/api/v3/quotes/index"
    response = requests.get(f"{url}?apikey={FMP_API_KEY}")
    if brief is True:
        indexes = []
        for dictionary in response.json():
            if dictionary['symbol'] in indexes_brief:
                indexes.append(dictionary)
        return indexes
    return response.json()


def get_fmp_quote(symbol):
    url = "https://financialmodelingprep.com/api/v3/quote"
    response = requests.get(f"{url}/{symbol}?apikey={FMP_API_KEY}")
    for dictionary in response.json():
        if dictionary['symbol'] == symbol:
            return dictionary
    raise Exception(f"Quote for {symbol} not found in response")


def get_gold_price():
    quote = get_fmp_quote(constants.FMP_GOLD_SYMBOL)
    return quote['price']


@lru_cache(maxsize=1)
def get_fmp_stock_symbol_universe():
    url = "https://financialmodelingprep.com/api/v3/stock/list"
    response = requests.get(f"{url}?apikey={FMP_API_KEY}")
    return response.json()


@lru_cache(maxsize=1)
def get_fmp_crypto_symbol_universe():
    url = "https://financialmodelingprep.com/api/v3/quotes/crypto"
    response = requests.get(f"{url}?apikey={FMP_API_KEY}")
    return response.json()


@lru_cache(maxsize=1)
def get_fmp_fx_symbol_universe():
    url = "https://financialmodelingprep.com/api/v3/fx"
    response = requests.get(f"{url}?apikey={FMP_API_KEY}")
    return response.json()


@lru_cache(maxsize=1)
def get_fmp_commodity_symbol_universe():
    url = "https://financialmodelingprep.com/api/v3/symbol/available-commodities"
    response = requests.get(f"{url}?apikey={FMP_API_KEY}")
    return response.json()


def is_symbol_in_iex_universe(symbol):
    for entry in get_iex_symbol_universe():
        if symbol == entry['symbol']:
            return True
    return False
