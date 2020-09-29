def calculate_sharpe_ratio(rate_of_return, risk_free_rate_of_return, excess_returns_std):
    # store sharpe ratio in a class variable
    sharpe_ratio = round((rate_of_return - risk_free_rate_of_return) / (excess_returns_std), 2)
    return sharpe_ratio


def calculate_sortino_ratio(rate_of_return, risk_free_rate_of_return, downside_returns_std):
    sortino_ratio = round((rate_of_return - risk_free_rate_of_return) / (downside_returns_std), 2)
    return sortino_ratio


def calculate_treynor_ratio(rate_of_return, risk_free_rate_of_return, beta):
    treynor_ratio = (rate_of_return - risk_free_rate_of_return) / beta
    return round(treynor_ratio, 2)


def calculate_calmar_ratio(rate_of_return, max_drawdown):
    calmar_ratio = rate_of_return / max_drawdown
    return round(calmar_ratio,2)
