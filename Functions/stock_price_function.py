import yfinance as yf
from datetime import datetime, timedelta

def get_stock_price (start_date, stock_code):

    stock_data = yf.Ticker(stock_code)
    end_date = start_date + timedelta(10)
    interval = '1d'
    stock = stock_data.history(start = start_date, end = end_date, auto_adjust= False)

    return stock

def main():
    date = datetime(2001,3,15)
    entry_date = '2020-03-13'
    date = datetime.strptime(entry_date, '%Y-%m-%d')
    stock_code = 'msft'
    stock = get_stock_price(date, stock_code)
    print(stock['Open'][datetime(2020, 3, 16)])

if __name__ == '__main__':
    main()