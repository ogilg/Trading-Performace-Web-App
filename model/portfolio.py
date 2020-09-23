from model.return_metrics import calculate_rate_of_return
import pandas as pd


# Stores a list of trades and calculates metrics with them
class Portfolio:
    def __init__(self, trades_list):
        self.trade_list = trades_list
        self.create_profit_list()
        self.find_total_amount_traded()
        self.find_total_exit_amount()

    def find_total_amount_traded(self):
        self.total_amount_traded = sum([trade.entry_capital for trade in self.trade_list])
        return self.total_amount_traded

    def find_total_exit_amount(self):
        self.total_exit_amount = sum([trade.exit_capital for trade in self.trade_list])
        return self.total_exit_amount

    def find_rate_of_return(self):
        self.rate_of_returns = calculate_rate_of_return(self.total_amount_traded, self.total_exit_amount)
        self.profit_factor = 1 + self.rate_of_returns
        return self.rate_of_returns

    def create_profit_list(self):
        for trade in self.trade_list:
            trade.calculate_profit()
        self.profits = [trade.profit for trade in self.trade_list]

    def calculate_total_profit(self):
        total_profit = sum(self.profits)
        assert (isinstance(total_profit, float))
        return total_profit

    def get_asset_list_from_trades(self):
        asset_list = list(dict.fromkeys([trade.asset for trade in self.trade_list]))
        return asset_list

    def calculate_aggregate_profit_by_day(self):
        for trade in self.trade_list:
            trade.calculate_profit_by_day()
        aggregate_daily_profit = self.trade_list[0].daily_profits
        for trade in self.trade_list[1:]:
            aggregate_daily_profit.add(trade.daily_profits, fill_value=0)

        print(self.trade_list[1].daily_profits.head())
        return aggregate_daily_profit

    # FILTERING
    def get_trades_by_asset(self, asset):
        return filter(lambda trade: trade.asset == asset, self.trade_list)
