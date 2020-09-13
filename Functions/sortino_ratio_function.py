def get_sortino_ratio (rate_of_return, risk_free_rate_of_return, stdev_of_DOWNSIDE_returns):
    """Return the Sortino ratio of the portfolio or of a particular stock (though not advised to do this)"""
    sortino_ratio = round((rate_of_return - risk_free_rate_of_return)/(stdev_of_DOWNSIDE_returns),2)
    if sortino_ratio<1:
        print(f"Your Sortino ratio is {sortino_ratio}, this is classified as sub-optimal")
    elif 2>sortino_ratio>1:
        print(f"Your Sortino ratio is {sortino_ratio}, this is classified as acceptable")
    elif sortino_ratio>2:
        print(f"Your Sortino ratio is {sortino_ratio}, this is classified as good")

