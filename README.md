# Automatic trading bot for cryptocurrency on Binance

## Introduction

This is a simple trading bot for cryptocurrency on Binance. It is written in Python and uses the Binance API. The strategy is based on the Stochastic RSI indicator. It is a simple strategy that can be used to make money on the cryptocurrency market. It is not a very good strategy, but it is a good starting point to learn how to write a trading bot.

## Setup

### API 

First you need to write your API key and secret in the '.env' file. You can find them in your Binance account.
They should be declared like this:

    SYMBOL_API_KEY=your_api_key
    SYMBOL_API_SECRET=your_api_secret

where SYMBOL is the symbol of the cryptocurrency you want to trade, for example you want to trade Bitcoin against USDT, symbol is BTCUSDT.

### Requirements

Then you need to install the requirements. You can do it by running the following command:

    pip install -r requirements.txt

### Config

Then you need to set up the parameters of the bot in a config file located in the 'config' folder. A config file is a JSON file with the following structure:

    {
        "interval": "4h",
        "symbol": "BNBUSDT",
        "date_start": "2022-06-01",
        "nb_periods_RSI": 11,
        "stochastic_length": 11,
        "smoothK": 2,
        "smoothD": 2,
        "nb_usdt": 100,
        "stop_loss": 10,
        "leverage": 2,
        "periods_MA": 400
    }

## Usage

To run the code, execute the following command:

    python MainStochRSI.py config/config.json

Where config.json is the name of the config file you want to use.
