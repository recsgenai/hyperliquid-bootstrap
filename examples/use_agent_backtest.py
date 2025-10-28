"""Example: Run backtest on CSV with an AI model (uses placeholder if no API keys).
Prepare a CSV 'data/sample_ohlcv.csv' with columns: timestamp,open,high,low,close,volume
"""
from bot.agent import get_model
from bot.backtester import run_backtest

model = get_model({'ai': {'model': 'placeholder'}})
out = run_backtest('data/sample_ohlcv.csv', model)
print('Report generated:', out['html'], out['pdf'])
