from model.return_metrics import calculate_rate_of_return

# Stores a list of trades and calculates metrics with them
class Portfolio:
    def __init__(self, trades_list):
        self.trade_list = trades_list
        self.create_profit_list()

    def find_total_amount_traded(self):
        self.total_amount_traded = sum([trade.entry_capital for trade in self.trade_list])
        return self.total_amount_traded

    def find_total_exit_amounts(self):
        self.total_exit_amount = sum([trade.exit_capital for trade in self.trade_list])
        return self.total_exit_amount

    def find_rate_of_return(self):
        self.rate_of_returns = calculate_rate_of_return(self.total_amount_traded, self.total_exit_amount)
        self.profit_factor = 1 + self.rate_of_returns
        return self.rate_of_returns

    def create_profit_list(self):
        map(lambda trade: trade.calculate_profit, self.trade_list)
        self.profits = [trade.profit for trade in self.trade_list]

    def calculate_win_rate(self):
        return len([profit >= 0 for profit in self.profits]) / len(self.trade_list)

    def calculate_total_profit(self):
        return sum(self.profits)


    # FILTERING
    def get_trades_by_asset(self, asset):
        return filter(lambda trade : trade.asset == asset, self.trade_list)
