def get_rate_of_return (starting_capital, finishing_capital):
    """Return the rate of return of the portfolio, or of an investment"""
    rate_of_return = (finishing_capital - starting_capital)/starting_capital
    print(f"Your rate of return is {rate_of_return*100}%")
