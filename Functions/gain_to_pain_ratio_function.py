def get_gain_to_pain_ratio (portfolio_gains, portfolio_losses):
    """Return the Gain to Pain ratio"""
    gain_to_pain_ratio = portfolio_gains / (abs(portfolio_losses))
    if gain_to_pain_ratio<1:
        print(f"Your Gain to Pain ratio is {gain_to_pain_ratio}, and is considered sub-optimal")
    elif 1<gain_to_pain_ratio<2:
        print(f"Your Gain to Pain ratio is {gain_to_pain_ratio}, and is considered good")
    elif 2<gain_to_pain_ratio<3:
        print(f"Your Gain to Pain ratio is {gain_to_pain_ratio}, and is considered excellent")
    else:
        print(f"Your Gain to Pain ratio is {gain_to_pain_ratio}, and is considered world-class")
        