from src.calculation.class_calculate import Calculate


class CalculateEMA(Calculate):

    @staticmethod
    def calculate_ema(historical, length1, length2):

        data = historical.copy()
        data['EMA_{}'.format(length1)] = data['close'].ewm(span=length1).mean()
        data['EMA_{}'.format(length2)] = data['close'].ewm(span=length2).mean()

        return data

    def buy_condition(self, buy_sell_df, i, length1=None, length2=None):
        return buy_sell_df['EMA_{}'.format(length1)][i] > buy_sell_df['EMA_{}'.format(length2)][i]

    def sell_condition(self, buy_sell_df, i, length1=None, length2=None):
        return buy_sell_df['EMA_{}'.format(length1)][i] < buy_sell_df['EMA_{}'.format(length2)][i]

    def calculate_buy_sell_table(self, historical, stop_loss, length1=None, length2=None):
        return super().calculate_buy_sell_table(
            CalculateEMA.calculate_ema(historical, length1, length2), stop_loss)
