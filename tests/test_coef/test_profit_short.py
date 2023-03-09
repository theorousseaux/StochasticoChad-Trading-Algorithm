import numpy as np
import sys
import os

sys.path.append(str(os.getcwd()))
# ATOM : 400, ENJ:180, WTC:600, VET: 150, BNB : 190
from src.position.strategy.stoch_rsi_strategy import StochRSIStrategy

NB_USDT = 100

symbol = sys.argv[1]
interval = "4h"
date_start = "2021-01-01"

api_key = "6ZBcjtqrZPEs3DLxl6Q7VIKSrssJp3Vgr1DKHUXON2g9RXY9n2VK0xI6AzUevKb0"
api_secret = "q1IY7H8xcweljMpD9wbHI5HVw8GBR1nF9VrPt9iqHYEAZWVzLtnNdoMnMzgRgUfX"


def calculate_profit(nb_periods_RSI, stochastic_length, smoothK, smoothD, stop_loss):
    position = StochRSIStrategy(symbol=symbol, interval=interval, date_start=date_start, api_key=api_key,
                                api_secret=api_secret, nb_usdt=NB_USDT,
                                nb_periods_RSI=nb_periods_RSI, stochasticLength=stochastic_length, smooth_K=smoothK,
                                smooth_D=smoothD, stop_loss=stop_loss, path="/")
    return position.buy_sell_df["efficiency trade"].sum()


nb_periods_RSI = 11
stochastic_length = 11
smoothK = 2
smoothD = 2
stop_loss = 10

def clean_db(data, i):
    db = data.copy()
    db["short"] = db["MA_{}".format(i)] > db['close']
    for i in range(len(db)):
        if db["efficiency short trade"][i] != 0:
            j = i - 1
            while db["flag"][j] == -1:
                j -= 1
            if not db.loc[db.index[j + 1], "short"]:
                db.loc[db.index[i], "efficiency short trade"] = 0
    return db


MA_range = np.arange(0, 801, 5)
profit = {}
profitmax = 0
for i in MA_range:
    position = StochRSIStrategy(symbol=symbol, interval=interval, date_start=date_start, api_key=api_key,
                                api_secret=api_secret, nb_usdt=NB_USDT,
                                nb_periods_RSI=nb_periods_RSI, stochasticLength=stochastic_length, smooth_K=smoothK,
                                smooth_D=smoothD, stop_loss=stop_loss, path="/", update_short=True,
                                periods_MA=i)
    db = clean_db(position.buy_sell_df, i)
    short_profit = db["efficiency short trade"].sum()
    profit[i] = short_profit
    if short_profit > profitmax:
        profitmax = short_profit
        with open("tests/test_coef/profit_short_{}.txt".format(sys.argv[1]), "a") as f:
            f.write("SHORT PROFIT MAX : {} / MA length : {}\n".format(profitmax, i))
    with open("tests/test_coef/profit_short_{}.txt".format(sys.argv[1]), "a") as f:
        f.write("MA length : {} / short profit = {}\n".format(i, short_profit))

with open("tests/test_coef/profit_short_{}.txt".format(sys.argv[1]), "a") as f:
    f.write(str(profit))
    f.write("\n")

position = StochRSIStrategy(symbol=symbol, interval=interval, date_start=date_start, api_key=api_key,
                            api_secret=api_secret, nb_usdt=NB_USDT,
                            nb_periods_RSI=nb_periods_RSI, stochasticLength=stochastic_length, smooth_K=smoothK,
                            smooth_D=smoothD, stop_loss=stop_loss, path="/", update_short=True,
                            periods_MA=190)

db = clean_db(position.buy_sell_df, 190)
with open("tests/test_coef/profit_short_{}.txt".format(sys.argv[1]), "a") as f:
    f.write(db["efficiency short trade"].sum())
    f.write("\n")
