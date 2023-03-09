import numpy as np

from Bot import class_position
from Bot import class_graph
import matplotlib.pyplot as plt

interval = "4h"
symbol = "BNBUSDT-study"
date_start = "2021-06-20"

nb_periods_RSI = 14
stochastic_length = 14
smoothK = 3
smoothD = 3

stop_loss = 10

date_start_list = ["2021-01-01", "2021-03-01", "2021-05-01", "2021-07-01"]

# rsi_length = np.arange(0, 21)

# plt.figure()
# for date in date_start_list:
#     efficiency = []
#     for i in rsi_length:
#         position = class_position.Position(symbol=symbol, interval=interval, date_start=date, nb_usdt=100,
#                                            nb_periods_RSI=i, stochasticLength=stochastic_length,
#                                            smooth_K=smoothK,
#                                            smooth_D=smoothD, stop_loss=stop_loss)
#         eff = position.buy_sell_stochastic_rsi_df["efficiency trade"].sum()
#         print(i, eff)
#         efficiency.append(eff)
#     plt.plot(rsi_length, efficiency, label=date)
#
# plt.ylabel("efficiency in percentage")
# plt.xlabel("RSI Length")
# plt.xticks(rsi_length)
# plt.title("Efficiency vs. rsi length")
# plt.legend()
# plt.savefig("{}/rsi_length_study".format(position.get_symbol()))
# plt.show()
# plt.close("all")

# stochastic_length_array = np.arange(0, 21)
# plt.figure()
# for date in date_start_list:
#     print(date)
#     efficiency = []
#     for i in stochastic_length_array:
#         position = class_position.Position(symbol=symbol, interval=interval, date_start=date, nb_usdt=100,
#                                            nb_periods_RSI=8, stochasticLength=i,
#                                            smooth_K=smoothK,
#                                            smooth_D=smoothD, stop_loss=stop_loss)
#         eff = position.buy_sell_stochastic_rsi_df["efficiency trade"].sum()
#         print(i, eff)
#         efficiency.append(eff)
#     plt.plot(stochastic_length_array, efficiency, label=date)
#
# plt.ylabel("efficiency in percentage")
# plt.xlabel("Stochastic Length")
# plt.xticks(rsi_length)
# plt.title("Efficiency vs. stochastic length")
# plt.legend()
# plt.savefig("{}/stochastic_length_study".format(position.get_symbol()))
# plt.show()
# plt.close("all")

# eff_array = np.zeros((len(rsi_length), len(stochastic_length_array)))
# for i in rsi_length:
#     for j in stochastic_length_array:
#         position = class_position.Position(symbol=symbol, interval=interval, date_start="2021-07-01", nb_usdt=100,
#                                            nb_periods_RSI=i, stochasticLength=j,
#                                            smooth_K=smoothK,
#                                            smooth_D=smoothD, stop_loss=stop_loss)
#         eff = position.buy_sell_stochastic_rsi_df["efficiency trade"].sum()
#         print(i, j)
#         print(eff)
#         eff_array[i, j] = eff
#
# plt.figure()
# plt.imshow(eff_array)
# plt.colorbar()
# plt.yticks(rsi_length)
# plt.ylabel("rsi length")
# plt.xticks(stochastic_length_array)
# plt.xlabel('stochastic lencth')
# plt.title("RSI and stochastic length influence")
# plt.show()
# plt.savefig("{}/stoch_rsi_length_study".format(position.get_symbol()))
#
# smoothD_array = np.arange(0, 10)
# plt.figure()
# for date in date_start_list:
#     print(date)
#     efficiency = []
#     for i in smoothD_array:
#         position = class_position.Position(symbol=symbol, interval=interval, date_start=date, nb_usdt=100,
#                                            nb_periods_RSI=9, stochasticLength=9,
#                                            smooth_K=smoothK,
#                                            smooth_D=i, stop_loss=stop_loss)
#         eff = position.buy_sell_stochastic_rsi_df["efficiency trade"].sum()
#         print(i, eff)
#         efficiency.append(eff)
#     plt.plot(smoothD_array, efficiency, label=date)
#
# plt.ylabel("efficiency in percentage")
# plt.xlabel("Smooth D length")
# plt.xticks(smoothD_array)
# plt.title("Efficiency vs. SmoothD length")
# plt.legend()
# plt.show()
# plt.close("all")
#
# smoothK_array = np.arange(0, 10)
# plt.figure()
# for date in date_start_list:
#     print(date)
#     efficiency = []
#     for i in smoothK_array:
#         position = class_position.Position(symbol=symbol, interval=interval, date_start=date, nb_usdt=100,
#                                            nb_periods_RSI=9, stochasticLength=9,
#                                            smooth_K=i,
#                                            smooth_D=3, stop_loss=stop_loss)
#         eff = position.buy_sell_stochastic_rsi_df["efficiency trade"].sum()
#         print(i, eff)
#         efficiency.append(eff)
#     plt.plot(smoothK_array, efficiency, label=date)
#
# plt.ylabel("efficiency in percentage")
# plt.xlabel("Smooth K length")
# plt.xticks(smoothD_array)
# plt.title("Efficiency vs. SmoothK length")
# plt.legend()
# plt.show()
# plt.close("all")

# eff_array = np.zeros((len(smoothK_array), len(smoothD_array)))
# for i in smoothK_array:
#     for j in smoothD_array:
#         position = class_position.Position(symbol=symbol, interval=interval, date_start="2021-03-01", nb_usdt=100,
#                                            nb_periods_RSI=9, stochasticLength=11,
#                                            smooth_K=i,
#                                            smooth_D=j, stop_loss=stop_loss)
#         eff = position.buy_sell_stochastic_rsi_df["efficiency trade"].sum()
#         print(i, j)
#         print(eff)
#         eff_array[i, j] = eff
#
# plt.figure()
# plt.imshow(eff_array)
# plt.colorbar()
# plt.yticks(smoothK_array)
# plt.ylabel("SmoothK length")
# plt.xticks(smoothD_array)
# plt.xlabel('SmoothD length')
# plt.title("Smooth K and D length influence")
# plt.show()
