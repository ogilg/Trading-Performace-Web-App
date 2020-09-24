from model.return_metrics import calculate_rate_of_return
import yfinance as yf
from datetime import datetime
import pandas as pd
from model.date_utils import date_range


class Trade:
    # dates in datetime format
    def __init__(self, asset_name, entry_date, exit_date, buy_price, number_of_shares):
        self.asset_name = asset_name
        self.buy_price = float(buy_price)
        self.number_of_shares = number_of_shares
        self.retrieve_entry_and_exit_dates(entry_date, exit_date)
        self.sell_price = self.find_sell_price()

    def retrieve_entry_and_exit_dates(self, entry_date, exit_date):
        self.entry_date = datetime.strptime(entry_date.split('T')[0], '%Y-%m-%d')
        self.exit_date = datetime.strptime(exit_date.split('T')[0], '%Y-%m-%d')

    def find_sell_price(self):
        self.stock_history = self.retrieve_yfinance_data()
        if self.data_fetch_successful:
            # take last close price
            exit_price = self.stock_history['Close'][-1]
            return exit_price

    def retrieve_yfinance_data(self):
        stock_history = self.fetch_stock_history()
        if self.data_fetch_successful:
            stock_history.drop(['Dividends', 'Stock Splits'], axis=1)

        return stock_history

    def fetch_stock_history(self):
        stock_ticker = yf.Ticker(self.asset_name)
        stock_history = stock_ticker.history(start=self.entry_date, end=self.exit_date, auto_adjust=False)
        if len(stock_history) == 0:  # catch when "No data found"
            self.data_fetch_successful = False
        else:
            self.data_fetch_successful = True
        return stock_history

    def calculate_profit(self):
        self.profit = round((self.sell_price - self.buy_price) * self.number_of_shares, 2)
        print(self.buy_price, self.sell_price)
        self.win = self.profit > 0

    def find_rate_of_return(self):
        self.rate_of_return = calculate_rate_of_return(self.buy_price, self.sell_price)
        self.profit_factor = 1 + self.rate_of_return
        return self.rate_of_return

    def calculate_profit_by_day(self):
        daily_profits = []

        for day in date_range(self.entry_date, self.exit_date):
            day = datetime.fromordinal(day.toordinal())
            try:
                day_profit = self.generate_day_profit_dict(day)
                daily_profits.append(day_profit)
            except KeyError:
                # skip weekends
                pass
        self.daily_profits = pd.DataFrame(daily_profits).set_index('Date')

    def generate_day_profit_dict(self, day):
        day_profit_open = (self.stock_history['Open'][day] - self.buy_price) * self.number_of_shares
        day_profit_close = (self.stock_history['Close'][day] - self.buy_price) * self.number_of_shares
        day_profit = {'Date': day, 'Profit Open': day_profit_open, 'Profit Close': day_profit_close}
        return day_profit
