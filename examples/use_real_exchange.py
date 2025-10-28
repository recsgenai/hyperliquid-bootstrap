"""Example: How to initialize a real exchange connector and fetch a ticker.
IMPORTANT: Keep your API keys local and never commit them to git.
Use environment variables, or an encrypted local store.
"""
import os
from bot.connectors.binance import BinanceConnector

def demo():
    # set env variables or pass keys explicitly
    # os.environ['BINANCE_API_KEY'] = 'your_key'
    # os.environ['BINANCE_API_SECRET'] = 'your_secret'
    b = BinanceConnector(testnet=True)
    print('Ticker:', b.fetch_ticker('BTC/USDT'))

if __name__ == '__main__':
    demo()
