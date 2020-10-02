import yfinance as yf
from datetime import timedelta


def get_t_bill_price(start_date):
    end_date = start_date + timedelta(1)
    tbill_data = yf.Ticker('^IRX')
    tbill = tbill_data.history(start=start_date, end=end_date, interval='1d', auto_adjust=False)
    t_bill_return = tbill['Close'][-1]
    return t_bill_return
