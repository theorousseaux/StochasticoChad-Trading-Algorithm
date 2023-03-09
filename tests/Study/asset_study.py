import class_position
import os
import numpy as np

interval = "4h"
# secure : BNB, AVAX, ADA, XRP, VET, DOT, EOS
# Avax, OMG, REP (prochains)
# SOL, BNB, WTC, VET, ADA, AVAX, DASH, ENJ, EOS, FIRO, OMG, QTUM, REP, XRP
symbol = "AVAXUSDT"
date_start = "2021-01-01"

api_key = '2F57uscVIhrAnbS79S3XmDxFb3is8b5KB3a6OHHK7ZMXQPlrVcvf7PPZdqvF57c6'
api_secret = 'oe5LRGQC6RPbrLyr6zyDFHdPHhI8ImdESXj6Z6irYFO2SSEoPLmFbWKkHw2kCt1v'

nb_periods_RSI = 9
stochastic_length = 11
smoothK = 2
smoothD = 2

nb_usdt = 15
stop_loss = 10

asset_list = ["BNBUSDT", "AVAXUSDT", "ADAUSDT", "XRPUSDT", "VETUSDT", "DOTUSDT", "EOSUSDT", "OMGUSDT", "REPUSDT",
              "WTCUSDT", "ENJUSDT", "FIROUSDT", "QTUMUSDT"]
eff = {}

for asset in asset_list:
    position = class_position.Position(symbol=asset, interval=interval, date_start=date_start, api_key=api_key,
                                       api_secret=api_secret, nb_usdt=nb_usdt,
                                       nb_periods_RSI=nb_periods_RSI, stochasticLength=stochastic_length,
                                       smooth_K=smoothK,
                                       smooth_D=smoothD, stop_loss=stop_loss)
    eff[asset] = position.buy_sell_df["efficiency trade"].sum()
