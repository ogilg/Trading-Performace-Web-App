class TradingSession:
    def __init__(self, trades_list, start_date, end_date):
        self.trades_list = trades_list
        self.start_date = start_date
        self.end_date = end_date

    def calculate_win_rate(self):
        # use trade.win (true if trade is a win, false otherwise)
        pass

    def calculate_metric(self, metric):
        # pass in a metric and apply it to trades
        pass

