def get_benchmark_gap_comparison_PORTFOLIO( rate_of_return_STOCK, benchmark_rate_of_return_SPECIFIC_INDUSTRY):
    """Return the performance gap between a stock and it's particular industry"""
    benchmark_gap_comparison_STOCK = rate_of_return_STOCK - benchmark_rate_of_return_SPECIFIC_INDUSTRY
    elif benchmark_gap_comparison_STOCK>0:
        print(f"You are outperforming the stock's industry by {benchmark_gap_comparison_STOCK}%")
    elif benchmark_gap_comparison_STOCK<0:
        print(f"You are underperforming the stock's industry by {abs(benchmark_gap_comparison_STOCK)}%")