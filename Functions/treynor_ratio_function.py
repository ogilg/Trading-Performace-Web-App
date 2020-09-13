def get_treynor_ratio (rate_of_return, risk_free_rate_of_return, beta):
    """Return the Treynor ratio for the portfolio or for a particular stock"""
    treynor_ratio = (rate_of_return - risk_free_rate_of_return)/beta
    print(f"For the Treynor ratio, comparison is the only way to use this number, so compare the ratio for 2 stocks or portfolios. The higher the Sortino ratio the better")

## Must create separate function which compares Treynor ratios for X values, or if easier just code for up to 3 values using option-type in function)