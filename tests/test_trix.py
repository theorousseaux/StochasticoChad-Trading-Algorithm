import os
from pathlib import Path
import sys

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
from src.position.strategy.trix_strategy import TrixStrategy

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

###
api_key = "6ZBcjtqrZPEs3DLxl6Q7VIKSrssJp3Vgr1DKHUXON2g9RXY9n2VK0xI6AzUevKb0"
api_secret = "q1IY7H8xcweljMpD9wbHI5HVw8GBR1nF9VrPt9iqHYEAZWVzLtnNdoMnMzgRgUfX"

path = ""

nb_usdt = 100

stop_loss = 10
symbol = "BNBUSDT"
interval = "1h"
leverage = 2

# if not os.path.exists("{}/".format(symbol)):
#     os.mkdir("{}/".format(symbol))
#
# with open("{}/trade-{}.txt".format(symbol, symbol), "a") as fichier:
#     fichier.write("pair : {} \n".format(symbol))
#     fichier.write("interval : {} \n".format(interval))
#     fichier.write("leverage : {} \n \n".format(leverage))

position = TrixStrategy(symbol=symbol, interval=interval, date_start="2022-11-01", api_key=api_key,
                        api_secret=api_secret, nb_usdt=nb_usdt, trixLength=7,
                        trixSignal=15, stop_loss=stop_loss, path=path, short=True)
position.update_buy_sell_trix_df()
df = position.buy_sell_df

buy_profit = df["efficiency trade"].sum()
sell_profit = df["efficiency short trade"].sum()

print("Long profit = " + str(round(buy_profit, 2)) + " %")
print("Short profit = " + str(round(sell_profit, 2)) + " %")
print("Total = " + str(round(buy_profit + sell_profit, 2)) + " %")

# position.save_graph()


###

# api = APIMargin(api_key, api_secret)
# [lot_size, price_filter] = api.get_precision_asset(symbol)
# quantity_precision = int(- np.log10(float(lot_size['stepSize'])))
# price_precision = int(- np.log10(float(price_filter['tickSize'])))
# quantity = round(nb_usdt / position.historical['close'][len(position.historical) - 1],
#                  quantity_precision)
#
# sell_short_market_order, short_stop_loss_limit, quantity_sold = ManageOrder.short_margin_with_sl(
#     api=api, symbol=symbol, quantity=quantity, leverage=leverage,
#     stop_loss=stop_loss, price_precision=price_precision, path="")
#
# print(sell_short_market_order)
#
# short_stop_loss_limit = api.get_order(symbol, short_stop_loss_limit)
# ManageOrder.buy_repay_margin(api=api, symbol=symbol, short_stop_loss_limit=short_stop_loss_limit,
#                              sell_short_market_order=sell_short_market_order,
#                              quantity_sold=quantity_sold,
#                              update_usdt=False,
#                              nb_usdt=nb_usdt,
#                              profit=[0], path=path)

#%%
