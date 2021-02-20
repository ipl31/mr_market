from prettytable import PrettyTable
from mister_market.helpers import commaify


class QuotePrettyTable:

    def __init__(self, quote):
        self.symbol = quote.symbol
        self.rows = [("Gainz", f"{quote.change_percentage}%"),
                     ("Price", commaify(quote.price)),
                     ("Open", commaify(quote.open)),
                     ("Prev Close", commaify(quote.previous_close)),
                     ("Day High", commaify(quote.high_day)),
                     ("Day Low", commaify(quote.low_day)),
                     ("52 H", commaify(quote.high_52w)),
                     ("52 L", commaify(quote.low_52w)),
                     ("200 MA", "%.2f" % quote.price_avg_200d)]

    def build_table(self):
        pt = PrettyTable()
        pt.align = 'l'
        for record in self.rows:
            if record[1] is None:
                self.rows.remove(record)
        pt.field_names = [r[0] for r in self.rows]
        pt.add_row([r[1] for r in self.rows])
        return pt.get_string(title=self.symbol)
