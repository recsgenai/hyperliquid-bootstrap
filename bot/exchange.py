import random
from dataclasses import dataclass

@dataclass
class Order:
    side: str
    price: float
    size: float

class SimulatedExchange:
    def __init__(self, symbol='BTC-USD', initial_price=30000.0, volatility=0.02):
        self.symbol = symbol
        self.price = initial_price
        self.volatility = volatility

    def get_market_snapshot(self):
        # Simulate small price movement and compute a simple trend
        shock = random.gauss(0, self.volatility) * self.price
        old_price = self.price
        self.price = max(0.1, self.price + shock)
        trend = (self.price - old_price) / old_price
        return {'symbol': self.symbol, 'price': self.price, 'trend': trend, 'volatility': self.volatility}

    def place_order(self, order: Order):
        # In a real connector, send the order to the exchange.
        # Here we simply return a simulated filled order.
        executed = {
            'side': order.side,
            'price': order.price,
            'size': order.size,
            'fee': abs(order.price * order.size) * 0.0007
        }
        return executed
