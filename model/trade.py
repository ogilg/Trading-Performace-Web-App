from model.return_metrics import calculate_rate_of_return
import yfinance as yf
from datetime import datetime
import pandas as pd
from model.date_utils import date_range


class Trade:
    # dates in datetime format
    def __init__(self, asset_name, entry_date, exit_date, entry_capital):
        self.asset_name = asset_name
        self.entry_capital = float(entry_capital)
        self.entry_date = datetime.strptime(entry_date.split('T')[0], '%Y-%m-%d')
        self.exit_date = datetime.strptime(exit_date.split('T')[0], '%Y-%m-%d')
        self.stock_history = self.retrieve_yfinance_data()
        self.number_of_shares = self.get_number_of_shares()
        self.exit_capital = self.get_exit_capital_from_yfinance()

    def get_exit_capital_from_yfinance(self):
        # take last close price
        exit_price = self.stock_history['Close'][-1]
        return exit_price * self.number_of_shares

    def get_number_of_shares(self):
        start_price = self.stock_history['Open'][0]
        number_of_shares = round(self.entry_capital / start_price)
        return number_of_shares

    def retrieve_yfinance_data(self):
        stock_ticker = yf.Ticker(self.asset_name)
        stock_history = stock_ticker.history(start=self.entry_date, end=self.exit_date, auto_adjust=False)
        stock_history.drop(['Adj Close', 'Dividends', 'Stock Splits'], axis=1)
        assert (len(stock_history) > 0)
        return stock_history

    def calculate_profit(self):
        self.profit = self.exit_capital - self.entry_capital
        self.win = self.profit > 0

    def find_rate_of_return(self):
        self.rate_of_return = calculate_rate_of_return(self.entry_capital, self.exit_capital)
        self.profit_factor = 1 + self.rate_of_return
        return self.rate_of_return

    def calculate_profit_by_day(self):
        daily_profits = []

        for day in date_range(self.entry_date, self.exit_date):
            day = datetime.fromordinal(day.toordinal())
            try:
                day_profit_open = self.stock_history['Open'][day] * self.number_of_shares - self.entry_capital
                day_profit_close = self.stock_history['Close'][day] * self.number_of_shares - self.entry_capital
                day_profit = {'Date': day, 'Profit Open': day_profit_open, 'Profit Close': day_profit_close}
                daily_profits.append(day_profit)
            except KeyError:
                # skip weekends
                pass
        self.daily_profits = pd.DataFrame(daily_profits).set_index('Date')
