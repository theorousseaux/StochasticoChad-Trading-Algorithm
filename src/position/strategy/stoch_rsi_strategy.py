from src.calculation.class_calculate_stoch_rsi import CalculateStochRSI
from src.position.class_position import Position
from src.graph.class_graph_stoch_rsi import CreateGraphStochRSI


class StochRSIStrategy(Position):
    def __init__(self, nb_usdt, symbol, interval, date_start, api_key, api_secret, stop_loss, path,
                 nb_periods_RSI,
                 stochasticLength,
                 smooth_K, smooth_D, periods_MA=0, update_short=False, update_usdt=False):
        super().__init__(nb_usdt=nb_usdt, symbol=symbol, interval=interval, date_start=date_start, api_key=api_key,
                         api_secret=api_secret, update_usdt=update_usdt, stop_loss=stop_loss, path=path,
                         trade_type='margin')

        # strategy parameters
        self.nb_periods_RSI = nb_periods_RSI
        self.stochasticLength = stochasticLength
        self.smooth_K = smooth_K
        self.smooth_D = smooth_D

        self._update_short = update_short
        self.periods_MA = periods_MA

        self.calculate = CalculateStochRSI()
        self.get_buy_sell_stochastic_rsi_df()

    ### update data ###

    def get_buy_sell_stochastic_rsi_df(self):
        self.get_historical()
        self.historical.drop(self.historical.tail(2).index,
                             inplace=True)
        self.buy_sell_df = self.calculate.calculate_buy_sell_table(
            historical=self.historical,
            nb_periods_RSI=self.nb_periods_RSI,
            stochasticLength=self.stochasticLength,
            smooth_K=self.smooth_K,
            smooth_D=self.smooth_D, stop_loss=self.stop_loss)

        if self._update_short:
            self.buy_sell_df = self.calculate.calculate_MA(historical=self.buy_sell_df,
                                                           nb_periods=self.periods_MA)
            self.short = self.buy_sell_df['close'][-1] < \
                         self.buy_sell_df['MA_{}'.format(self.periods_MA)][-1]

    def update_buy_sell_stochastic_rsi_df(self):
        self.update_last_interval()
        self.buy_sell_df = self.calculate.calculate_buy_sell_table(
            historical=self.historical,
            nb_periods_RSI=self.nb_periods_RSI,
            stochasticLength=self.stochasticLength,
            smooth_K=self.smooth_K,
            smooth_D=self.smooth_D, stop_loss=self.stop_loss)

    def update_all(self):
        self.update_buy_sell_stochastic_rsi_df()
        if self._update_short:
            self.buy_sell_df = self.calculate.calculate_MA(historical=self.buy_sell_df,
                                                           nb_periods=self.periods_MA)
            self.short = self.buy_sell_df['close'][-1] < \
                         self.buy_sell_df['MA_{}'.format(self.periods_MA)][-1]

    def save_graph(self):
        CreateGraphStochRSI.plot_rsi(self.buy_sell_df.tail(100), self.interval, self.symbol,
                                     self.path)
        CreateGraphStochRSI.plot_stochastic_rsi_entry_exit(self.buy_sell_df.tail(100),
                                                           self.interval, self.symbol, self.path)
