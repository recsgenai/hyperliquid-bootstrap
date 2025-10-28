class RiskManager:
    def __init__(self, config):
        self.config = config
        self.starting_balance = config.get('general', {}).get('starting_balance', 10000.0)
        self.max_drawdown_pct = config.get('trading', {}).get('max_drawdown_pct', 20.0)
        self.min_balance = self.starting_balance * (1 - self.max_drawdown_pct/100)
        self.current_drawdown_protection = False

    def position_size(self, balance, price, risk_pct):
        # Simple fixed fractional sizing
        risk_amount = balance * (risk_pct/100.0)
        size = risk_amount / price
        return size

    def check_drawdown(self, balance):
        if balance <= self.min_balance:
            self.current_drawdown_protection = True
            return False
        return True
