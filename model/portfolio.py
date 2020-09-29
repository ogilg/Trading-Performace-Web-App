from model.return_metrics import calculate_rate_of_return


# Stores a list of trades and calculates metrics with them
class Portfolio:
    def __init__(self, trades_list):
        self.trade_list = trades_list
        self.create_profit_list()

    def find_total_amount_traded(self):
        self.total_amount_traded = sum([trade.buy_price * trade.number_of_shares for trade in self.trade_list])
        return self.total_amount_traded

    def find_total_exit_amount(self):
        self.total_exit_amount = sum([trade.sell_price * trade.number_of_shares for trade in self.trade_list])
        return self.total_exit_amount

    def find_rate_of_return(self):
        self.rate_of_returns = calculate_rate_of_return(self.total_amount_traded, self.total_exit_amount)
        self.profit_factor = 1 + self.rate_of_returns
        return self.rate_of_returns

    def create_profit_list(self):
        for trade in self.trade_list:
            trade.calculate_profit()
        self.profits = [trade.profit for trade in self.trade_list]

    def get_asset_list_from_trades(self):
        asset_list = list(dict.fromkeys([trade.asset_name for trade in self.trade_list if trade.data_fetch_successful]))
        return asset_list

    def calculate_aggregate_profit_by_day(self):
        for trade in self.trade_list:
            trade.calculate_profit_by_day()
        aggregate_daily_profit = self.trade_list[0].daily_profits
        for trade in self.trade_list[1:]:
            aggregate_daily_profit.add(trade.daily_profits, fill_value=0)

        return aggregate_daily_profit
