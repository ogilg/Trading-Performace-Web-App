import numpy as np

def calculate_sharpe_ratio(rate_of_return, risk_free_rate_of_return, excess_returns_std):
    sharpe_ratio = (rate_of_return - risk_free_rate_of_return) / (excess_returns_std)
    return round(sharpe_ratio * np.sqrt(252), 2)


def calculate_sortino_ratio(rate_of_return, risk_free_rate_of_return, downside_returns_std):
    sortino_ratio = (rate_of_return - risk_free_rate_of_return) / (downside_returns_std)
    return round(sortino_ratio, 2)


def calculate_treynor_ratio(rate_of_return, risk_free_rate_of_return, beta):
    treynor_ratio = (rate_of_return - risk_free_rate_of_return) / beta
    return round(treynor_ratio, 2)


def calculate_calmar_ratio(rate_of_return, max_drawdown):
    calmar_ratio = rate_of_return / max_drawdown
    return round(calmar_ratio, 2)
