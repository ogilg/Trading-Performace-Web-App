def get_calmar_ratio (rate_of_return, max_drawdown):
    """Return the Calmar ratio"""
    calmar_ratio = rate_of_return / max_drawdown
    if calmar_ratio<0.50:
        print(f"Your Calmar ratio is {calmar_ratio}, this is considered sub-optimal")
    elif 0.50<calmar_ratio<3.0:
        print(f"Your Calmar ratio is {calmar_ratio}, this is considered good")
    elif 3.0<calmar_ratio<5.0:
        print(f"Your Calmar ratio is {calmar_ratio}, this is considered excellent")
