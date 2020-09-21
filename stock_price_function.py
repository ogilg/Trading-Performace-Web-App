import yfinance as yf
from datetime import datetime, timedelta

def get_stock_price (date, stock_code):

    stock_data = yf.Ticker(stock_code)
    start_date = date
    end_date = start_date + timedelta(1)
    interval = '1d'
    stock = stock_data.history(start = start_date, end = end_date, interval = interval, auto_adjust= False)
    stock_price = stock['Close']
    print(stock_price)
    return stock_price


date = datetime(2001,3,15)
stock_code = 'msft'
stock_price = get_stock_price(date, stock_code)