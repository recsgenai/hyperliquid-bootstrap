import yaml, time
from .exchange import SimulatedExchange, Order
from .agent import AIModelPlaceholder
from .risk import RiskManager
from .journal import TradeJournal

class Runner:
    def __init__(self, config_path='config.yaml'):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.exchange = SimulatedExchange(symbol=self.config['trading']['symbol'])
        self.agent = AIModelPlaceholder(self.config)
        self.risk = RiskManager(self.config)
        self.journal = TradeJournal()
        self.balance = self.config['general']['starting_balance']
        self.position = 0.0
        self.avg_entry = None

    def run_simulation(self, steps=100):
        for step in range(steps):
            snap = self.exchange.get_market_snapshot()
            signal = self.agent.analyze(snap)
            print(f"step={step:03d} price={snap['price']:.2f} trend={snap['trend']:.4f} -> {signal.action} (c={signal.confidence:.2f})")

            # risk controls
            if not self.risk.check_drawdown(self.balance):
                print("Drawdown protection triggered — stopping trading.")
                break

            if signal.action == 'buy':
                size = self.risk.position_size(self.balance, snap['price'], self.config['trading']['risk_per_trade_pct'])
                order = Order(side='buy', price=snap['price'], size=size)
                executed = self.exchange.place_order(order)
                self.journal.record(executed, reason='ai_buy')
                # simple accounting
                cost = executed['price'] * executed['size'] + executed['fee']
                self.balance -= cost
                # track position
                self.position += executed['size']
                self.avg_entry = executed['price'] if self.avg_entry is None else (self.avg_entry + executed['price'])/2
            elif signal.action == 'sell' and self.position > 0:
                size = self.position
                order = Order(side='sell', price=snap['price'], size=size)
                executed = self.exchange.place_order(order)
                self.journal.record(executed, reason='ai_sell')
                proceeds = executed['price'] * executed['size'] - executed['fee']
                self.balance += proceeds
                self.position = 0.0
                self.avg_entry = None

            time.sleep(0.01)

        print('\nSimulation finished. Balance:', round(self.balance,2))
        df = self.journal.to_dataframe()
        if not df.empty:
            print(df.describe(include='all'))