def get_expectancy (win_rate, ave_win_size, ave_loss_size):
    """Return the expectancy of the portfolio"""
    expectancy = (win_rate*ave_win_size) - (1-win_rate)*abs(ave_loss_size)
    if expectancy>0:
        print(f"Your overall expectancy (what you can expect to make on each trade) is positive, you win on average {expectancy}£ per trade")
    elif expectancy <0:
        print(f"Your overall expectancy (what you can expect to make on each trade) is negative, you lose on average {abs(expectancy)}£ per trade. Consider changing your trading strategy")
    else:
        print(f"Your overall expectancy is 0, this means on average you neither win nor lose money on each trade. Consider changing your trading strategy")
