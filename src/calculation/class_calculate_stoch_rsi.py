from src.calculation.class_calculate import Calculate


class CalculateStochRSI(Calculate):

    @staticmethod
    def calculate_rsi(historical, nb_periods_RSI):

        data = historical.copy()
        # Calculate Price Differences
        data['diff'] = data['close'].diff(1)

        # Calculate Avg. Gains/Losses
        data['gain'] = data['diff'].clip(lower=0).round(4)
        data['loss'] = data['diff'].clip(upper=0).abs().round(4)

        # Get initial Averages
        data['avg_gain'] = data['gain'].rolling(window=nb_periods_RSI, min_periods=nb_periods_RSI).mean()[
                           :nb_periods_RSI + 1]
        data['avg_loss'] = data['loss'].rolling(window=nb_periods_RSI, min_periods=nb_periods_RSI).mean()[
                           :nb_periods_RSI + 1]

        # Get WMS averages
        # Average Gains
        for i, row in enumerate(data['avg_gain'].iloc[nb_periods_RSI + 1:]):
            data['avg_gain'].iloc[nb_periods_RSI + 1 + i] = (data['avg_gain'].iloc[i + nb_periods_RSI] * (
                    nb_periods_RSI - 1) +
                                                             data['gain'].iloc[
                                                                 i + nb_periods_RSI + 1]) / nb_periods_RSI

        # Average Losses
        for i, row in enumerate(data['avg_loss'].iloc[nb_periods_RSI + 1:]):
            data['avg_loss'].iloc[nb_periods_RSI + 1 + i] = (data['avg_loss'].iloc[i + nb_periods_RSI] * (
                    nb_periods_RSI - 1) +
                                                             data['loss'].iloc[
                                                                 i + nb_periods_RSI + 1]) / nb_periods_RSI

        # Calculate RS Values
        data['rs'] = data['avg_gain'] / data['avg_loss']

        # Calculate RSI
        data['rsi'] = 100 - (100 / (1.0 + data['rs']))

        return data

    @staticmethod
    def calculate_stochastic_rsi(historical, nb_periods_RSI, stochasticLength, smooth_K, smooth_D):
        rsi = CalculateStochRSI.calculate_rsi(historical, nb_periods_RSI)
        data = rsi.copy()[['open', 'high', 'low', 'close', 'rsi']]

        # calcul of fast stoch rsi
        data["fastStochRSI"] = 100 * (
                data["rsi"] - data['rsi'].rolling(window=stochasticLength, min_periods=stochasticLength).min()) / (
                                       data['rsi'].rolling(window=stochasticLength,
                                                           min_periods=stochasticLength).max() - data['rsi'].rolling(
                                   window=stochasticLength, min_periods=stochasticLength).min())

        # we smooth the fast stoch rsi
        data["%K"] = data["fastStochRSI"].rolling(window=smooth_K).mean()

        # calcul of %D line
        data["%D"] = data["%K"].rolling(window=smooth_D).mean()

        return data

    def buy_condition(self, buy_sell_df, i):
        if i == 0:
            return False
        return (buy_sell_df['%K'][i] > buy_sell_df['%D'][i]) & (
                (buy_sell_df['%K'][i] < 20) | (buy_sell_df['%K'][i - 1] < 20))

    def sell_condition(self, buy_sell_df, i):
        if i == 0:
            return False
        return (buy_sell_df['%K'][i] < buy_sell_df['%D'][i]) & (
                (buy_sell_df['%K'][i] > 80) | (buy_sell_df['%K'][i - 1] > 80))

    def calculate_buy_sell_table(self, historical, stop_loss, nb_periods_RSI=None, stochasticLength=None, smooth_K=None,
                                 smooth_D=None):
        return super().calculate_buy_sell_table(
            CalculateStochRSI.calculate_stochastic_rsi(historical, nb_periods_RSI, stochasticLength, smooth_K,
                                                       smooth_D), stop_loss)

    @staticmethod
    def calculate_MA(historical, nb_periods):

        data = historical.copy()
        # Calculate moving average
        data['MA_{}'.format(nb_periods)] = data['close'].rolling(nb_periods).mean()

        return data
