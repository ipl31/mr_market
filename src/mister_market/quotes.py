import os
import fmpsdk

FMP_API_KEY = os.environ["FMP_API_KEY"]


class FmpQuote:
    """ Provides an interface implementation for getting Quotes from FMP. FMP
        supports Stocks, Crypto and Commodities through the quote API.
    """

    def __init__(self, ticker_symbol):
        self.symbol = ticker_symbol
        response = fmpsdk.quote(FMP_API_KEY, self.symbol)
        if len(response) > 1:
            msg = f"Unexpected Value. FMP API returned " \
                  f"mutliple records for non-batch quote: {self.symbol}"
            raise ValueError(msg)
        data = response[0]
        self.name = data["name"]
        self.price = data["price"]
        self.change_percentage = data["changesPercentage"]
        self.change_value = data["change"]
        self.low_day = data["dayLow"]
        self.high_day = data["dayHigh"]
        self.low_52w = data["yearLow"]
        self.high_52w = data["yearHigh"]
        self.volume_day = data["volume"]
        self.volume_avg = data["avgVolume"]
        self.open = data["open"]
        self.previous_close = data["previousClose"]
        self.pe_ratio = data["pe"]
        self.market_cap = data["marketCap"]
        self.price_avg_50d = data["priceAvg50"]
        self.price_avg_200d = data["priceAvg200"]
