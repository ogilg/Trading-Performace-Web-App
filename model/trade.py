from model.return_metrics import calculate_rate_of_return
import yfinance as yf
from datetime import datetime, timedelta


class Trade:
    # dates in datetime format
    def __init__(self, asset_name, entry_date, exit_date):
        self.asset_name = asset_name
        self.entry_date = entry_date
        self.exit_date = exit_date
        self.stock_history = self.retrieve_yfinance_data()
        self.exit_capital = self.get_exit_capital_from_yfinance()

    def set_entry_amount(self, entry_capital):
        # stores entry capital in class variable, it becomes accessible anywhere in the class
        self.entry_capital = entry_capital

    def get_exit_capital_from_yfinance(self):
        exit_capital = self.stock_history['Close']
        return exit_capital

    def retrieve_yfinance_data(self):
        stock_ticker = yf.Ticker(self.asset_name)
        return stock_ticker.history(start=self.entry_date, end=self.entry_date, auto_adjust=False)

    def calculate_profit(self):
        self.profit = self.exit_capital() - self.entry_capital
        self.win = self.profit > 0

    def find_rate_of_return(self):
        self.rate_of_return = calculate_rate_of_return(self.entry_capital, self.exit_capital())
        self.profit_factor = 1 + self.rate_of_return
        return self.rate_of_return
