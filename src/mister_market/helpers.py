import os
import requests
from . import constants
from functools import lru_cache
from iexfinance import refdata


def commaify(data):
    if data is None:
        return data
    return "{:,}".format(data)


@lru_cache(maxsize=1)
def get_iex_symbol_universe():
    return refdata.get_symbols(output_format='json')


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

    key = os.environ["FMP_API_KEY"]
    url = "https://financialmodelingprep.com/api/v3/quotes/index"
    response = requests.get(f"{url}?apikey={key}")
    if brief is True:
        indexes = []
        for dictionary in response.json():
            if dictionary['symbol'] in indexes_brief:
                indexes.append(dictionary)
        return indexes
    return response.json()


def get_fmp_quote(symbol):
    key = os.environ["FMP_API_KEY"]
    url = "https://financialmodelingprep.com/api/v3/quote"
    response = requests.get(f"{url}/{symbol}?apikey={key}")
    for dictionary in response.json():
        if dictionary['symbol'] == symbol:
            return dictionary
    raise Exception(f"Quote for {symbol} not found in response")


def get_gold_price():
    quote = get_fmp_quote(constants.GOLD_COMM_SYMBOL)
    return quote['price']


def is_symbol_in_iex_universe(symbol):
    for entry in get_iex_symbol_universe():
        if symbol == entry['symbol']:
            return True
    return False
