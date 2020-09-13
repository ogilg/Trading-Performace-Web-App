def get_sharpe_ratio (rate_of_return, risk_free_rate_of_return, stdev_of_EXCESS_returns):
    """Return the Sharpe ratio of the portfolio or of a particular stock (though not advised to do this)"""
    sharpe_ratio = round((rate_of_return - risk_free_rate_of_return)/(stdev_of_EXCESS_returns),2)
    if sharpe_ratio<1:
        print(f"Your Sharpe ratio is {sharpe_ratio}, this is classified as sub-optimal")
    elif 2>sharpe_ratio>1:
        print(f"Your Sharpe ratio is {sharpe_ratio}, this is classified as good")
    elif 3>sharpe_ratio>2:
        print(f"Your Sharpe ratio is {sharpe_ratio}, this is classified as very good")
    elif sharpe_ratio>3:
        print(f"Your Sharpe ratio is {sharpe_ratio}, this is classified as excellent")

