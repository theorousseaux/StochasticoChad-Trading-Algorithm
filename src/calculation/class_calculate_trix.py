from src.calculation.class_calculate import Calculate

import ta


class CalculateTRIX(Calculate):

    @staticmethod
    def calculate_trix(historical, trixLength, trixSignal):

        data = historical.copy()

        trixLength = trixLength
        trixSignal = trixSignal

        data['TRIX'] = ta.trend.ema_indicator(
            ta.trend.ema_indicator(ta.trend.ema_indicator(close=data['close'], window=trixLength), window=trixLength),
            window=trixLength)
        data['TRIX_PCT'] = data["TRIX"].pct_change() * 100
        data['TRIX_SIGNAL'] = ta.trend.sma_indicator(data['TRIX_PCT'], trixSignal)
        data['TRIX_HISTO'] = data['TRIX_PCT'] - data['TRIX_SIGNAL']

        # -- Stochasitc RSI --
        data['STOCH_RSI'] = ta.momentum.stochrsi(close=data['close'], window=14, smooth1=3, smooth2=3)

        return data

    def buy_condition(self, buy_sell_df, i):
        return buy_sell_df['TRIX_HISTO'][i] > 0 and buy_sell_df['STOCH_RSI'][i] < 0.8

    def sell_condition(self, buy_sell_df, i):
        return buy_sell_df['TRIX_HISTO'][i] < 0 and buy_sell_df['STOCH_RSI'][i] > 0.2

    def calculate_buy_sell_table(self, historical, stop_loss, trixLength=None, trixSignal=None):
        return super().calculate_buy_sell_table(CalculateTRIX.calculate_trix(historical, trixLength, trixSignal), stop_loss)
