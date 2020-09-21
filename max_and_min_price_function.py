import yfinance as yf
from datetime import datetime, timedelta

def get_max_and_min_price (start_date, end_date, stock_code):
    stock_data = yf.Ticker(stock_code)
    interval = '1d'
    stock = stock_data.history(start=start_date, end=end_date, interval=interval, auto_adjust=False)
    stock_price = stock['Close']
    print(stock_price)
    max_and_min = sorted(stock_price, reverse=True)
    print(max_and_min[0])
    print(max_and_min[-1])

#test data
start_date = datetime(2020,1,1)
end_date = datetime(2020,9,20)
stock_code = 'MSFT'
max_and_min  = get_max_and_min_price(start_date,end_date,stock_code)