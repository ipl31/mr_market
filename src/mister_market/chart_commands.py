import requests
from datetime import datetime, timedelta
from iexfinance.stocks import get_historical_data
from .plugin_base import PluginBase
from .slack import BlockBuilder


# TODO: No longer using quickcharts python client. Remove it.


def get_daily_prices_year(symbol):
    end = datetime.now()
    start = end - timedelta(days=365)
    return get_historical_data(symbol, start, end=end)


QUICKCHART_URL = 'https://quickchart.io/chart/create'


class QuickChartsChart(object):

    def __init__(self, dataset, ylabel, xlabel,
                 height=300, width=500, type="line"):
        self.height = height
        self.width = width
        self.type = type
        # x axis labels
        self.xlabel = xlabel
        self.dataset = dataset
        # self.api_key = os.environ["QUICKCHARTS_API_KEY"]
        # TODO Fix when implemented
        self.api_key = None
        self.qc_url = f"{QUICKCHART_URL}?{self.api_key}"

        self.config = {"width": self.width,
                       "height": self.height,
                       "chart": {
                           "type": self.type,
                           "data": {
                               # dates
                               "labels": self.xlabel,
                               "datasets": [{
                                   "label": ylabel,
                                   "data": self.dataset
                               }]
                           }
                       }
                       }

    def get_url(self):
        response = requests.post(self.qc_url, json=self.config)
        chart_response = response.json()
        return chart_response['url']


def create_52w_graph(symbol):
    data = get_daily_prices_year(symbol)
    dataset = []
    ylabels = []
    for date in data:
        ylabels.append(date)
        dataset.append(data[date]['close'])
    chart = QuickChartsChart(dataset, ylabels, symbol)
    return chart.get_url()


class ChartCommand(PluginBase):
    command = "chart"
    usage = "chart $symbol"
    description = "request chart"

    def __init__(self):
        pass

    def run(self, *args, **kwargs):
        args = list(args)
        symbol = args.pop[0]
        bb = BlockBuilder()
        graph_url = create_52w_graph(symbol)
        bb.add_image_block(graph_url, graph_url, f"{symbol} chart")
        return bb.product
