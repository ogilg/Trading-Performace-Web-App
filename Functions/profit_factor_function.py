def get_profit_factor (rate_of_return):
    """Return the profit factor"""
    profit_factor = 1+rate_of_return
    if profit_factor>1:
        print(f"Your profit factor is {profit_factor}; meaning for every dollar invested you have received on average {profit_factor}$. As this is over one, your trading is profitable")
    else:
        print(f"Your profit factor is {profit_factor}; meaning for every dollar invested you have received on average {profit_factor}$. Which means on average you lost {1-profit_factor}$. As this is under one, your trading is not profitable, you are losing money")
