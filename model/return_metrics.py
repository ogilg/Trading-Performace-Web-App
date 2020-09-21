
def calculate_rate_of_return(entry_capital, exit_capital):
    rate_of_return = (exit_capital() - entry_capital) / entry_capital
    return rate_of_return

def find_day_high(stock_day_history):
    return stock_day_history['High']

def find_day_low(stock_day_history):
    return stock_day_history['Low']

def find_stock_high(stock_history):
    return max(stock_history['High'])

def find_stock_low(stock_history):
    return min(stock_history['Low'])


