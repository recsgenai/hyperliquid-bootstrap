"""Bybit connector wrapper (ccxt)."""

import os
try:
    import ccxt
except Exception:
    ccxt = None

class BybitConnector:
    def __init__(self, api_key=None, api_secret=None, testnet=True):
        if ccxt is None:
            raise RuntimeError("ccxt not installed. Run: pip install ccxt")
        self.api_key = api_key or os.getenv('BYBIT_API_KEY')
        self.api_secret = api_secret or os.getenv('BYBIT_API_SECRET')
        self.testnet = testnet
        self.client = ccxt.bybit({'apiKey': self.api_key, 'secret': self.api_secret, 'enableRateLimit': True})
        if self.testnet:
            self.client.set_sandbox_mode(True)

    def fetch_ticker(self, symbol):
        return self.client.fetch_ticker(symbol)

    def create_order(self, symbol, side, type_, amount, price=None, params=None):
        return self.client.create_order(symbol, type_, side, amount, price, params or {})

    def fetch_balance(self):
        return self.client.fetch_balance()
