"""Connector wrapper for Binance (spot & futures) using ccxt.
Requires: pip install ccxt
Keys must remain local (e.g., .env or encrypted local storage).
"""
import os
try:
    import ccxt
except Exception as e:
    ccxt = None

class BinanceConnector:
    def __init__(self, api_key=None, api_secret=None, testnet=True):
        if ccxt is None:
            raise RuntimeError("ccxt library not installed. Run: pip install ccxt")
        self.api_key = api_key or os.getenv('BINANCE_API_KEY')
        self.api_secret = api_secret or os.getenv('BINANCE_API_SECRET')
        self.testnet = testnet
        self._init_client()

    def _init_client(self):
        self.client = ccxt.binance({
            'apiKey': self.api_key,
            'secret': self.api_secret,
            'enableRateLimit': True,
        })
        if self.testnet:
            # switch to testnet/futures if needed
            self.client.set_sandbox_mode(True)

    def fetch_ticker(self, symbol):
        return self.client.fetch_ticker(symbol)

    def create_order(self, symbol, side, type_, amount, price=None, params=None):
        # type_ = 'limit' or 'market'
        return self.client.create_order(symbol, type_, side, amount, price, params or {})

    def fetch_balance(self):
        return self.client.fetch_balance()
