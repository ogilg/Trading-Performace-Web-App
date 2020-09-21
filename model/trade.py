from model.return_metrics import calculate_rate_of_return


class Trade:
    def __init__(self, asset_name, entry_date, exit_date):
        self.asset_name = asset_name
        self.entry_date = entry_date
        self.exit_date = exit_date

    def set_entry_amount(self, entry_capital):
        # stores entry capital in class variable, it becomes accessible anywhere in the class
        self.entry_capital = entry_capital

    # TODO: implement by retrieving appropriate data
    def get_exit_capital(self):
        # Use stock data to calculate
        self.exit_capital = 10
        pass

    def calculate_profit(self):
        self.profit = self.get_exit_capital() - self.entry_capital
        self.win = self.profit > 0

    def find_rate_of_return(self):
        self.rate_of_return = calculate_rate_of_return(self.entry_capital, self.exit_capital())
        self.profit_factor = 1 + self.rate_of_return
        return self.rate_of_return
