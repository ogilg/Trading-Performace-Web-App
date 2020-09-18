
class Trade:
    def __init__(self, asset_name, entry_date, exit_date):
        self.asset_name = asset_name
        self.entry_date = entry_date
        self.exit_date = exit_date

    def set_entry_amount(self, entry_capital):
        # stores entry capital in class variable, it becomes accessible anywhere in the class
        self.entry_capital = entry_capital

    def get_exit_capital(self):
        # Use stock data to calculate
        pass

    def calculate_profit(self):
        self.profit = self.get_exit_capital() - self.entry_capital
        self.win = self.profit > 0

    def calculate_rate_of_return(self):
        self.rate_of_return = (self.get_exit_capital() - self.entry_capital) / self.entry_capital
        self.profit_factor = 1 + self.rate_of_return
        return self.rate_of_return

    # RATIOS
    def calculate_sharpe_ratio(self, rate_of_return, risk_free_rate_of_return, excess_returns_std):
        # store sharpe ratio in a class variable
        self.sharpe_ratio = round((rate_of_return - risk_free_rate_of_return) / (excess_returns_std), 2)
        return self.sharpe_ratio

    def calculate_sortino_ratio(self, rate_of_return, risk_free_rate_of_return, downside_returns_std):
        self.sortino_ratio = round((rate_of_return - risk_free_rate_of_return) / (downside_returns_std), 2)
        return self.sortino_ratio

    def calculate_treynor_ratio(self, rate_of_return, risk_free_rate_of_return, beta):
        self.treynor_ratio = (rate_of_return - risk_free_rate_of_return) / beta
        return self.treynor_ratio

    def calculate_calmar_ratio(self, rate_of_return, max_drawdown):
        self.calmar_ratio = rate_of_return / max_drawdown
        return self.calmar_ratio



example_trade = Trade('GOOG', 01-01-2020, 01-02-2020)

print(example_trade.asset_name) # should print 'GOOG'
example_trade.set_entry_amount(100)
print(example_trade.entry_capital) # should print 100





