
class Trade:
    def __init__(self, asset_name, entry_date, exit_date):
        self.asset_name = asset_name
        self.entry_date = entry_date
        self.exit_date = exit_date

    def set_entry_amount(self, entry_amount):
        self.entry_amount = entry_amount

    def get_exit_amount(self):
        # Use stock data to calculate
        pass

    def calculate_profit(self):
        self.profit = self.get_exit_amount() - self.entry_amount
        self.win = self.profit > 0  

