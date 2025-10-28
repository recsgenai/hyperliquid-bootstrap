import pandas as pd
from datetime import datetime

class TradeJournal:
    def __init__(self):
        self.trades = []

    def record(self, executed_order, reason=''):
        row = {
            'timestamp': datetime.utcnow(),
            'side': executed_order['side'],
            'price': executed_order['price'],
            'size': executed_order['size'],
            'fee': executed_order.get('fee', 0.0),
            'reason': reason
        }
        self.trades.append(row)

    def to_dataframe(self):
        return pd.DataFrame(self.trades)
