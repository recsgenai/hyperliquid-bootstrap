"""Simple backtester that reads OHLCV CSV and runs the agent over historical steps.
Produces an HTML report and a simple PDF snapshot using matplotlib.
CSV expected columns: timestamp,open,high,low,close,volume
"""
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime
from .journal import TradeJournal

def load_ohlcv(csv_path):
    df = pd.read_csv(csv_path, parse_dates=['timestamp'])
    df = df.sort_values('timestamp').reset_index(drop=True)
    return df

def run_backtest(csv_path, model, starting_balance=10000.0, risk_pct=1.0):
    df = load_ohlcv(csv_path)
    balance = starting_balance
    position = 0.0
    avg_entry = None
    journal = TradeJournal()

    for idx, row in df.iterrows():
        snapshot = {'price': row['close'], 'trend': (row['close'] - row['open'])/row['open'] if row['open']>0 else 0, 'volatility': 0}
        sig = model.analyze(snapshot)
        if sig.action == 'buy':
            size = (balance * (risk_pct/100.0)) / snapshot['price']
            executed = {'side':'buy','price':snapshot['price'],'size':size,'fee':snapshot['price']*size*0.0007}
            journal.record(executed, reason='backtest_buy')
            cost = executed['price']*executed['size'] + executed['fee']
            balance -= cost
            position += executed['size']
            avg_entry = executed['price'] if avg_entry is None else (avg_entry+executed['price'])/2
        elif sig.action == 'sell' and position>0:
            executed = {'side':'sell','price':snapshot['price'],'size':position,'fee':snapshot['price']*position*0.0007}
            journal.record(executed, reason='backtest_sell')
            proceeds = executed['price']*executed['size'] - executed['fee']
            balance += proceeds
            position = 0.0
            avg_entry = None

    # close leftover position at last price
    if position>0:
        last_price = df.iloc[-1]['close']
        executed = {'side':'sell','price':last_price,'size':position,'fee':last_price*position*0.0007}
        journal.record(executed, reason='backtest_close')
        balance += executed['price']*executed['size'] - executed['fee']

    # generate reports
    out_dir = os.path.join(os.getcwd(), 'backtest_reports')
    os.makedirs(out_dir, exist_ok=True)
    timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    html_path = os.path.join(out_dir, f'report_{timestamp}.html')
    pdf_path = os.path.join(out_dir, f'report_{timestamp}.pdf')

    df_trades = journal.to_dataframe()
    # HTML
    html = f"<h1>Backtest report</h1><p>Starting balance: {starting_balance}</p><p>Ending balance: {balance:.2f}</p>"
    html += df_trades.to_html(index=False)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)

    # Simple PDF snapshot via matplotlib
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axis('off')
    text = f"Backtest report\nStarting: {starting_balance}\nEnding: {balance:.2f}\nTrades: {len(df_trades)}"
    ax.text(0.01, 0.99, text, va='top', fontsize=10)
    fig.savefig(pdf_path)
    plt.close(fig)

    return {'html': html_path, 'pdf': pdf_path, 'trades_df': df_trades}
