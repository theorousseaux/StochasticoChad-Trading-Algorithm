import numpy as np


class Calculate:

    @staticmethod
    def calculate_MA(historical, nb_periods):

        data = historical.copy()
        # Calculate moving average
        data['MA_{}'.format(nb_periods)] = data['close'].rolling(nb_periods).mean()

        return data

    def buy_condition(self, df, i):
        pass

    def sell_condition(self, df, i):
        pass

    def calculate_buy_sell_table(self, historical, stop_loss):

        buy = []
        sell = []

        efficiency = np.NaN
        efficiency_short = np.NaN

        efficiency_list = []
        efficiency_trade_list = []

        efficiency_short_list = []
        efficiency_trade_short_list = []

        flag = 0
        flag_list = []

        price_bought = 0
        price_sell = np.NaN

        for i in range(len(historical)):
            efficiency_trade = np.NaN
            efficiency_trade_short = np.NaN

            # if we are in trade we calculate the current efficiency
            if flag == 1:
                efficiency = 100 * (historical.iloc[i]['close'] - price_bought) / price_bought
                efficiency_list.append(efficiency)
                efficiency_short_list.append(np.NaN)
            elif flag == -1:
                efficiency_short = -(100 * (historical.iloc[i]['close'] - price_sell) / price_sell)
                efficiency_short_list.append(efficiency_short)
                efficiency_list.append(np.NaN)
            else:
                efficiency_list.append(np.NaN)
                efficiency_short_list.append(np.NaN)

            # then we check the stop loss condition and close the trade in this case
            if flag == -1:
                SLS = ((historical.iloc[i]['high'] - price_sell) / price_sell) * 100 > stop_loss
                SL = False
            elif flag == 1:
                SL = ((historical.iloc[i]['low'] - price_bought) / price_bought) * 100 < - stop_loss
                SLS = False
            else:
                SL = False
                SLS = False

            if (flag == 1) & ((stop_loss != 0) & SL):
                buy.append(np.NaN)
                sell.append(historical.iloc[i]['close'])
                flag = 0
                efficiency_trade = efficiency

            elif (flag == -1) & ((stop_loss != 0) & SLS):
                buy.append(historical.iloc[i]['close'])
                sell.append(np.NaN)
                flag = 0
                efficiency_trade_short = efficiency_short

            elif self.buy_condition(historical, i):
                sell.append(np.NaN)

                # if are not in trade we buy
                if (flag == 0) | (flag == -1):
                    buy.append(historical.iloc[i]['close'])
                    if flag == -1:
                        efficiency_trade_short = efficiency_short
                    flag = 1
                    price_bought = historical.iloc[i]['close']
                else:
                    buy.append(np.NaN)

            # check if D line cross K line
            elif self.sell_condition(historical, i):
                buy.append(np.NaN)

                # if we are in trade, we sell
                if (flag == 1) | (flag == 0):
                    sell.append(historical.iloc[i]['close'])
                    if flag == 1:
                        efficiency_trade = efficiency
                    flag = -1
                    price_sell = historical.iloc[i]['close']
                else:
                    sell.append(np.NaN)

            else:
                sell.append(np.NaN)
                buy.append(np.NaN)
            efficiency_trade_list.append(efficiency_trade)
            efficiency_trade_short_list.append(efficiency_trade_short)
            flag_list.append(flag)

        historical["buy"] = buy
        historical["sell"] = sell

        historical["efficiency"] = efficiency_list
        historical["efficiency trade"] = efficiency_trade_list

        historical["efficiency short"] = efficiency_short_list
        historical["efficiency short trade"] = efficiency_trade_short_list
        historical["flag"] = flag_list

        return historical
