import os
import sys

sys.path.append(os.getcwd())

from src.position.strategy.stoch_rsi_strategy import StochRSIStrategy
from dotenv import load_dotenv
from src.position.manage_order import ManageOrder

load_dotenv()

interval = "4h"

symbol = "TRBUSDT"
date_start = "2023-09-01"

api_key = os.getenv("TEST_API_KEY")
api_secret = os.getenv("TEST_API_SECRET")

nb_periods_RSI = 11
stochastic_length = 11
smoothK = 2
smoothD = 2

nb_usdt = 10
stop_loss = 10
leverage = 2

# if not os.path.exists("{}/".format(symbol)):
#     os.mkdir("{}/".format(symbol))
#
# with open("{}/trade-{}.txt".format(symbol, symbol), "a") as fichier:
#     fichier.write("pair : {} \n".format(symbol))
#     fichier.write("interval : {} \n".format(interval))
#     fichier.write("leverage : {} \n \n".format(leverage)

position = StochRSIStrategy(symbol=symbol, interval=interval, date_start=date_start, api_key=api_key,
                            api_secret=api_secret, nb_usdt=nb_usdt,
                            nb_periods_RSI=nb_periods_RSI, stochasticLength=stochastic_length, smooth_K=smoothK,
                            smooth_D=smoothD, periods_MA=600, stop_loss=stop_loss, path='', update_short=True)

buy_profit = position.buy_sell_df["efficiency trade"].sum()
sell_profit = position.buy_sell_df["efficiency short trade"].sum()
print(buy_profit)
print(sell_profit)
print(buy_profit + sell_profit)

