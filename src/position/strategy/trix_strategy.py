from src.calculation.class_calculate_trix import CalculateTRIX
from src.position.class_position import Position
from src.graph.class_graph_trix import CreateGraphTrix


class TrixStrategy(Position):
    def __init__(self, nb_usdt, symbol, interval, date_start, api_key, api_secret, stop_loss, path,
                 trixLength, trixSignal, short=False, update_usdt=False):
        super().__init__(nb_usdt=nb_usdt, symbol=symbol, interval=interval, date_start=date_start, api_key=api_key,
                         api_secret=api_secret, update_usdt=update_usdt, stop_loss=stop_loss, short=short, path=path,
                         trade_type='margin')

        # strategy parameters
        self.trixLength = trixLength
        self.trixSignal = trixSignal

        self.calculate = CalculateTRIX()
        self.get_buy_sell_trix_df()

     ### update data ###

    def get_buy_sell_trix_df(self):
        self.get_historical()
        self.historical.drop(self.historical.tail(2).index,
                             inplace=True)
        self.buy_sell_df = self.calculate.calculate_buy_sell_table(
            historical=self.historical,
            trixLength=self.trixLength,
            trixSignal=self.trixSignal,
            stop_loss=self.stop_loss)

    def update_buy_sell_trix_df(self):
        self.update_last_interval()
        self.buy_sell_df = self.calculate.calculate_buy_sell_table(
            historical=self.historical,
            trixLength=self.trixLength,
            trixSignal=self.trixSignal,
            stop_loss=self.stop_loss)

    def update_all(self):
        self.update_buy_sell_trix_df()

    def save_graph(self):
        CreateGraphTrix.plot_trix_entry_exit(self.buy_sell_df.tail(100), self.symbol, self.path)