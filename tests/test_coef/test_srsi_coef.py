import os
from pathlib import Path
import sys
import pickle
import numpy as np

sys.path.append(str(os.getcwd()))
from src.position.strategy.stoch_rsi_strategy import StochRSIStrategy

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

interval = "4h"
date_start = "2020-01-01"

api_key = "6ZBcjtqrZPEs3DLxl6Q7VIKSrssJp3Vgr1DKHUXON2g9RXY9n2VK0xI6AzUevKb0"
api_secret = "q1IY7H8xcweljMpD9wbHI5HVw8GBR1nF9VrPt9iqHYEAZWVzLtnNdoMnMzgRgUfX"

symbol = ["BNBUSDT", "ENJUSDT", "VETUSDT", "WTCUSDT", "ATOMUSDT", "EOSUSDT", "AVAXUSDT", "TRBUSDT"]
nb_periods_RSI = np.arange(5, 20)
stochastic_length = np.arange(5, 20)
smoothK = np.arange(2, 10)
smoothD = np.arange(2, 10)

nb_usdt = 10
stop_loss = np.arange(5, 21, 5)
leverage = 2


def calculate_profit(symbol, nb_periods_RSI, stochastic_length, smoothK, smoothD, stop_loss):
    while True:
        try:
            position = StochRSIStrategy(symbol=symbol, interval=interval, date_start=date_start, api_key=api_key,
                                        api_secret=api_secret, nb_usdt=nb_usdt,
                                        nb_periods_RSI=nb_periods_RSI, stochasticLength=stochastic_length,
                                        smooth_K=smoothK,
                                        smooth_D=smoothD, periods_MA=600, stop_loss=stop_loss, path='',
                                        update_short=True)
            break
        except Exception as e:
            print(e)
            pass
    buy_profit = position.buy_sell_df["efficiency trade"].sum()
    sell_profit = position.buy_sell_df["efficiency short trade"].sum()

    return buy_profit + sell_profit

dico = {}

for sy in symbol:
    profit_max = 0
    dico[sy] = profit_max
    for nb in nb_periods_RSI:
        for st in stochastic_length:
            for sk in smoothK:
                for sd in smoothD:
                    for sl in stop_loss:
                        profit = calculate_profit(sy, nb, st, sk, sd, sl)
                        if profit > profit_max:
                            profit_max = profit
                            dico[sy] = {'Profit max': profit_max, 'nb_periods_RSI': nb, 'stochastic_length': st, 'SmoothK': sk, 'SmoothD': sd, "SL": sl}
                            with open("coef_update.txt".format(symbol, symbol), "a") as fichier:
                                fichier.write("Profit max = {} | param : {}, {}, {}, {}, {} \n Stop loss = {} \n".format(profit_max, sy, nb, st, sk, sd, sl))
                                fichier.write(str(dico) + '\n')

with open("profit_data.pkl", "wb") as tf:
    pickle.dump(dico, tf)

## Read it
with open("profit_data.pkl", "wb") as tf:
    new_dict = pickle.load(tf)

print(new_dict.item())
