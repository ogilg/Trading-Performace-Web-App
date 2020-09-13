
class Trade:
    def __init__(self, asset_name, entry_date, exit_date):
        self.asset_name = asset_name
        self.entry_date = entry_date
        self.exit_date = exit_date

    def set_entry_amount(self, entry_capital):
        self.entry_capital = entry_capital

    def get_exit_capital(self):
        # Use stock data to calculate
        pass

    def calculate_profit(self):
        self.profit = self.get_exit_capital() - self.entry_capital
        self.win = self.profit > 0

    def get_rate_of_return(self):
        self.rate_of_return = (self.get_exit_capital() - self.entry_capital) / self.entry_capital
        print(f"Your rate of return is {self.rate_of_return * 100}%")
        return self.rate_of_return

