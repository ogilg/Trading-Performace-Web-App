from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf

from helper_functions.date_utils import date_range
from helper_functions.date_utils import remove_day_time
from helper_functions.return_metrics import calculate_rate_of_return


class Trade:
    # dates in datetime format
    def __init__(self, asset_name, entry_date, exit_date, buy_price, number_of_shares):
        self.asset_name = asset_name
        self.buy_price = float(buy_price)
        self.number_of_shares = number_of_shares
        self.retrieve_entry_and_exit_dates(entry_date, exit_date)
        self.sell_price = self.find_sell_price()

    def retrieve_entry_and_exit_dates(self, entry_date, exit_date):
        self.entry_date = datetime.strptime(remove_day_time(entry_date), '%Y-%m-%d')
        self.exit_date = datetime.strptime(remove_day_time(exit_date), '%Y-%m-%d')

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
        self.win = self.profit > 0

    def find_rate_of_return(self):
        self.rate_of_return = calculate_rate_of_return(self.buy_price, self.sell_price)
        self.profit_factor = 1 + self.rate_of_return
        return self.rate_of_return

    def calculate_stock_price_by_day(self):
        daily_closes = []

        for day in date_range(self.entry_date, self.exit_date + timedelta(1)):
            day = datetime.fromordinal(day.toordinal())
            try:
                day_close = self.generate_trade_prices(day)
                daily_closes.append(day_close)
            except KeyError:
                # skip weekends
                pass
        self.daily_close_list = pd.DataFrame(daily_closes).set_index('Date')

    def generate_trade_prices(self, day):
        day_trade_close = (self.stock_history['Close'][day]) * self.number_of_shares
        day_close = {'Date': day, 'Stock Close': day_trade_close}
        return day_close
