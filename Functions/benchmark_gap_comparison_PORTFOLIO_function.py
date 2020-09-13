def get_benchmark_gap_comparison_PORTFOLIO(rate_of_return_PORTFOLIO, benchmark_rate_of_return_SP500):
    """Return the performance gap between the portfolio and the S&P500"""
    benchmark_gap_comparison_PORTFOLIO = rate_of_return_PORTFOLIO - benchmark_rate_of_return_SP500
    if benchmark_gap_comparison_PORTFOLIO>0:
        print(f"You are outperforming the S&P500 by {benchmark_gap_comparison_PORTFOLIO}%")
    else:
        print(f"You are underperforming the S&P500 by {abs(benchmark_gap_comparison_PORTFOLIO)}%")

