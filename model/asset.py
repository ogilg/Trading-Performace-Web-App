class AssetTrades:
    def __init__(self, trades_list, asset_name):
        self.trades_list = trades_list
        self.asset_name = asset_name
        assert(len(self.trades_list) > 0)
        assert(self.trades_list[0].asset_name == self.asset_name) #check trade name is correct

    def calculate_win_rate(self):
        pass

    def get_stock_data(self):
        # use asset_name to fetch stock price data
        pass