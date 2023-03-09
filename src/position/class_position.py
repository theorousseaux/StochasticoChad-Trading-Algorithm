import os

import numpy as np
import pandas as pd

from src.binance_api.class_api_margin import APIMargin
from src.binance_api.class_api_spot import API
from src.position.class_time import Time
from src.position.manage_order import ManageOrder


class Position:
    flag_dic = {-1: "short", 0: "waiting", 1: "long"}

    def __init__(self, nb_usdt, symbol, interval, date_start, api_key, api_secret, update_usdt=False, stop_loss=0, short=False, path="/", trade_type=None):
        self.symbol = symbol
        self.interval = interval
        self.date_start = date_start
        self.profit = []

        # connexion
        if trade_type == 'margin':
            self.api = APIMargin(api_key, api_secret)
        else:
            self.api = API(api_key, api_secret)

        # data
        self.historical = pd.DataFrame()
        self.get_historical()

        # manage time
        self.time_manager = Time(self.interval)

        # save files
        self.path = path

        # way to manage positions
        self.__nb_usdt = nb_usdt
        self.__update_usdt = update_usdt
        self.short = short
        self.stop_loss = stop_loss

        # initialize
        self.in_trade = "waiting"
        self.buy_sell_df = pd.DataFrame()

    ### getter ###

    def get_symbol(self):
        return self.symbol

    def get_interval(self):
        return self.interval

    def get_date_start(self):
        return self.date_start

    def get_profit(self):
        return self.profit

    def save_graph(self):
        pass

    ### update data ###

    def get_historical(self, volume=False):
        historical = self.api.get_historical(symbol=self.symbol, interval=self.interval,
                                             date_start=self.date_start)

        if volume:
            for line in historical:
                del line[6:]
            historical = pd.DataFrame(historical, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        else:
            for line in historical:
                del line[5:]
            historical = pd.DataFrame(historical, columns=['date', 'open', 'high', 'low', 'close'])

        historical = historical.astype(float)
        historical['date'] = pd.to_datetime(historical['date'], unit='ms')
        historical.set_index('date', inplace=True)
        self.historical = historical

    # adds the data from the last complete interval
    def update_last_interval(self):
        new_line = self.api.get_client().get_historical_klines(self.symbol, interval=self.interval,
                                                               start_str="8 hour ago UTC")[-2]
        del new_line[5:]
        new_serie = pd.Series(new_line, index=['date', 'open', 'high', 'low', 'close'])
        new_serie.name = pd.to_datetime(new_serie['date'], unit='ms')
        new_serie.drop('date', inplace=True)
        new_serie = new_serie.astype(float)
        self.historical = pd.concat([self.historical, new_serie.to_frame().T], ignore_index=False)

    def update_all(self):
        pass

    ### strategy to apply from our data ###

    def strategy_with_leverage(self, leverage=1):

        # we calculate precisions for round
        [lot_size, price_filter] = self.api.get_precision_asset(self.get_symbol())
        quantity_precision = int(- np.log10(float(lot_size['stepSize'])))
        price_precision = int(- np.log10(float(price_filter['tickSize'])))

        stop_loss_limit = {}
        short_stop_loss_limit = {}

        buy_market_order = {}
        sell_short_market_order = {}

        quantity_bought = 0
        quantity_sold = 0

        usdt_borrow = 0

        while True:

            start = self.time_manager.get_time()

            # display current time
            with open(self.path + "{}/trade-{}.txt".format(self.symbol, self.symbol), "a") as f:
                f.write("\n{} -> updating\n".format(self.time_manager.current_date()))

            # update
            while True:
                try:
                    self.update_all()
                    break
                except Exception as e:
                    print(e)
                    pass

            # if we have to short/long
            quantity = round(self.__nb_usdt / self.historical['close'][len(self.historical) - 1],
                             quantity_precision)

            # if we are in long
            if self.in_trade == "long":

                # we verify if the SL had been performed
                stop_loss_limit = self.api.get_order(self.symbol, stop_loss_limit)
                if stop_loss_limit['status'] == 'FILLED':
                    self.__nb_usdt, self.profit = ManageOrder.stop_loss_executed(symbol=self.symbol,
                                                                                 stop_loss_limit=stop_loss_limit,
                                                                                 buy_market_order=buy_market_order,
                                                                                 update_usdt=self.__update_usdt,
                                                                                 nb_usdt=self.__nb_usdt,
                                                                                 usdt_borrow=usdt_borrow,
                                                                                 profit=self.profit, path=self.path)
                    self.in_trade = Position.flag_dic[0]

                # if we have to sell
                elif self.buy_sell_df['flag'][len(self.buy_sell_df) - 1] == -1:
                    self.__nb_usdt, self.profit = ManageOrder.sell_repay_margin(api=self.api, symbol=self.symbol,
                                                                                stop_loss_limit=stop_loss_limit,
                                                                                buy_market_order=buy_market_order,
                                                                                quantity_bought=quantity_bought,
                                                                                usdt_borrow=usdt_borrow,
                                                                                update_usdt=self.__update_usdt,
                                                                                nb_usdt=self.__nb_usdt,
                                                                                profit=self.profit, path=self.path)
                    self.in_trade = Position.flag_dic[0]

                    # if we want to short
                    if self.short:
                        self.time_manager.wait(2)
                        sell_short_market_order, short_stop_loss_limit, quantity_sold = ManageOrder.short_margin_with_sl(
                            api=self.api, symbol=self.symbol, quantity=quantity, leverage=leverage,
                            stop_loss=self.stop_loss, price_precision=price_precision, path=self.path)
                        self.in_trade = Position.flag_dic[-1]

            # if we are in short
            elif self.in_trade == "short":
                # we verify if the SL had been performed
                short_stop_loss_limit = self.api.get_order(self.symbol, short_stop_loss_limit)
                if short_stop_loss_limit['status'] == 'FILLED':
                    self.__nb_usdt, self.profit = ManageOrder.short_stop_loss_executed(symbol=self.symbol,
                                                                                       short_stop_loss_limit=short_stop_loss_limit,
                                                                                       sell_short_market_order=sell_short_market_order,
                                                                                       update_usdt=self.__update_usdt,
                                                                                       nb_usdt=self.__nb_usdt,
                                                                                       profit=self.profit,
                                                                                       path=self.path)

                    self.in_trade = Position.flag_dic[0]

                # if we have to buy
                elif self.buy_sell_df['flag'][len(self.buy_sell_df) - 1] == 1:
                    self.__nb_usdt, self.profit = ManageOrder.buy_repay_margin(api=self.api, symbol=self.symbol,
                                                                               short_stop_loss_limit=short_stop_loss_limit,
                                                                               sell_short_market_order=sell_short_market_order,
                                                                               quantity_sold=quantity_sold,
                                                                               update_usdt=self.__update_usdt,
                                                                               nb_usdt=self.__nb_usdt,
                                                                               profit=self.profit, path=self.path)
                    self.time_manager.wait(2)

                    # then we buy as usual
                    buy_market_order, stop_loss_limit, quantity_bought, usdt_borrow = ManageOrder.buy_margin_with_sl(
                        api=self.api, symbol=self.symbol, quantity=quantity, leverage=leverage,
                        stop_loss=self.stop_loss, quantity_precision=quantity_precision,
                        price_precision=price_precision, path=self.path)
                    self.in_trade = Position.flag_dic[1]

            # if we are waiting
            else:
                # if we have to short
                if ((self.buy_sell_df['flag'][len(self.buy_sell_df) - 2] == 0) | (
                        self.buy_sell_df['flag'][len(self.buy_sell_df) - 2] == 1)) & (
                        self.buy_sell_df['flag'][
                            len(self.buy_sell_df) - 1] == -1) & self.short:
                    sell_short_market_order, short_stop_loss_limit, quantity_sold = ManageOrder.short_margin_with_sl(
                        api=self.api, symbol=self.symbol, quantity=quantity, leverage=leverage,
                        stop_loss=self.stop_loss, price_precision=price_precision, path=self.path)
                    self.in_trade = Position.flag_dic[-1]

                # if we have to buy
                elif ((self.buy_sell_df['flag'][len(self.buy_sell_df) - 2] == 0) | (
                        self.buy_sell_df['flag'][len(self.buy_sell_df) - 2] == -1)) & (
                        self.buy_sell_df['flag'][len(self.buy_sell_df) - 1] == 1):
                    buy_market_order, stop_loss_limit, quantity_bought, usdt_borrow = ManageOrder.buy_margin_with_sl(
                        api=self.api, symbol=self.symbol, quantity=quantity, leverage=leverage,
                        stop_loss=self.stop_loss, quantity_precision=quantity_precision,
                        price_precision=price_precision, path=self.path)
                    self.in_trade = Position.flag_dic[1]

            # we plot ans save data
            self.save_graph()

            if not os.path.exists(self.path + "{}/".format(self.symbol)):
                os.mkdir(self.path + "{}/".format(self.symbol))
            self.buy_sell_df.to_excel(
                excel_writer=self.path + "{}/entry_exit.xlsx".format(self.symbol))

            # display the current trade status
            if self.in_trade == "short":
                with open(self.path + "{}/trade-{}.txt".format(self.symbol, self.symbol), "a") as f:
                    f.write("{} -> short in progress \n".format(self.time_manager.current_date()))
            elif self.in_trade == "long":
                with open(self.path + "{}/trade-{}.txt".format(self.symbol, self.symbol), "a") as f:
                    f.write("{} -> long in progress \n".format(self.time_manager.current_date()))
            else:
                with open(self.path + "{}/trade-{}.txt".format(self.symbol, self.symbol), "a") as f:
                    f.write("{} -> NO trade in progress \n".format(self.time_manager.current_date()))

            end = self.time_manager.get_time()
            self.time_manager.wait_next_interval(end - start)
