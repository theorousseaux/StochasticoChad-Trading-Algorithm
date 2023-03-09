import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

import sys

sys.path.append('../../src/')

from Class import class_position

api_key = "6ZBcjtqrZPEs3DLxl6Q7VIKSrssJp3Vgr1DKHUXON2g9RXY9n2VK0xI6AzUevKb0"
api_secret = "q1IY7H8xcweljMpD9wbHI5HVw8GBR1nF9VrPt9iqHYEAZWVzLtnNdoMnMzgRgUfX"

symbol = "BNBUSDT"
interval = "4h"
date = "2021-12-01"

nb_periods_RSI = np.arange(5, 21)
stochastic_length = np.arange(5, 21)
smoothK = np.arange(2, 7)
smoothD = np.arange(2, 7)
stop_loss = 10


eff_max = 0
param_max = (0, 0, 0, 0)

for i in tqdm(nb_periods_RSI, desc="total progress"):
    for j in tqdm(stochastic_length, desc="stochastic progress"):
        for k in smoothK:
            position = class_position.Position(symbol=symbol, interval=interval, api_key=api_key, api_secret=api_secret, date_start=date, nb_usdt=100,
                                               nb_periods_RSI=i, stochasticLength=j,
                                               smooth_K=k,
                                               smooth_D=k, stop_loss=stop_loss)
            eff = position.buy_sell_df["efficiency trade"].sum()
            if eff > eff_max:
                eff_max = eff
                param_max = (i, j, k, k)
    print(eff_max)
    print(param_max)
