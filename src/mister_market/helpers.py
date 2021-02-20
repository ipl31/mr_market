import os

import fmpsdk
import requests
import yfinance as yf
from .constants import MisterMarketConstants
from functools import lru_cache
from iexfinance import refdata
from iexfinance.stocks import Stock
from tabulate import tabulate


FMP_API_KEY = os.environ["FMP_API_KEY"]
constants = MisterMarketConstants()


def commaify(data):
    if data is None:
        return data
    return "{:,}".format(data)


def get_options_expiration(symbol):
    stock = yf.Ticker(symbol)
    expirations = stock.options
    return expirations


def get_options_chains_near_strike_tabulated(symbol, expiration, strike):
    calls, puts = get_options_chains_near_strike(symbol, expiration, strike)
    calls = tabulate_options_dataframe(calls)
    puts = tabulate_options_dataframe(puts)
    return {"calls": calls, "puts": puts}


def get_options_chains_near_strike(symbol, expiration, strike):
    strike = float(strike)
    stock = yf.Ticker(symbol)
    calls = stock.option_chain(date=expiration).calls
    puts = stock.option_chain(date=expiration).puts
    # based on strike value look for options with strikes within 25% of value
    band = strike * 0.10
    calls = calls.loc[(calls["strike"] >= strike - band) &
                      (calls["strike"] <= strike + band)]
    puts = puts.loc[(puts["strike"] >= strike - band) &
                    (puts["strike"] <= strike + band)]
    calls = calls.round(2)
    puts = puts.round(2)
    calls = format_options_chains_dataframe(calls)
    puts = format_options_chains_dataframe(puts)
    return calls, puts


def format_options_chains_dataframe(dataframe):
    # remove unwanted columns and rename some columns for readability
    dataframe = dataframe.drop(columns=["contractSymbol",
                                        "inTheMoney",
                                        "contractSize",
                                        "currency",
                                        "lastTradeDate",
                                        "change",
                                        "percentChange",
                                        "volume"])
    dataframe = dataframe.rename(
        columns={"openInterest": "OI", "impliedVolatility": "IV"})
    return dataframe


def tabulate_options_dataframe(dataframe):
    table = tabulate(dataframe, headers="keys", tablefmt='pretty')
    return table


# TODO Finish this
"""
def fred_get_unemployment_csv(start=None, end=None):
    # Latest date is first in query param, beginning date is last
    if end is None:
        end = datetime.datetime.today()
    if start is None:
        start = "1948-01-01"
    url = ("https://fred.stlouisfed.org/graph/fredgraph.csv?"
           "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans"
           "&graph_bgcolor=%23ffffff&height=450&mode=fred"
           "&recession_bars=on&txtcolor=%23444444&ts=12&tts=12"
           "&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes"
           "&show_tooltip=yes&id=UNRATE&scale=left"
           "&cosd=1948-01-01&coed=2020-12-01"
           "&line_color=%234572a7&link_values=false"
           "&line_style=solid&mark_type=none&mw=3"
           "&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg"
           "&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin"
           "&vintage_date=2021-02-03&revision_date={}&nd={}")
"""


@lru_cache(maxsize=1)
def get_iex_symbol_universe():
    return refdata.get_symbols(output_format='json')


def get_iex_symbol_news(symbol, limit=5):
    stock = Stock(symbol, output_format='json')
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
def get_fmp_stock_universe():
    # Gets list of dicts with symbols, name, price and exchange.
    url = "https://financialmodelingprep.com/api/v3/stock/list"
    response = requests.get(f"{url}?apikey={FMP_API_KEY}")
    return response.json()


@lru_cache(maxsize=1)
def get_fmp_symbol_universe():
    # TODO: Switch this to use FMPSDK when bug fix is released:
    url = "https://financialmodelingprep.com/api/v3/quotes/crypto"
    cryptos = requests.get(f"{url}?apikey={FMP_API_KEY}").json()
    stocks = fmpsdk.symbols_list(FMP_API_KEY)
    commodities = fmpsdk.commodities_list(FMP_API_KEY)
    fx = fmpsdk.available_forex(FMP_API_KEY)
    # TODO: add other exchanges like TSX and Mutual funds etc...
    symbols = [s["symbol"] for s in stocks]
    symbols = symbols + [c["symbol"] for c in commodities]
    symbols = symbols + [c["symbol"] for c in cryptos]
    symbols = symbols + [f["symbol"] for f in fx]
    return symbols


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
