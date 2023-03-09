from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException


class API:
    def __init__(self, api_key, api_secret):
        self._api_key = api_key
        self._api_secret = api_secret
        self._client = Client(self._api_key, self._api_secret)

    def get_api_key(self):
        return self._api_key

    def get_api_secret(self):
        return self._api_secret

    def get_account(self):
        return self._client.get_account()

    def get_client(self):
        return self._client

    def get_historical(self, symbol, interval, date_start):
        return self._client.get_historical_klines(symbol=symbol, interval=interval, start_str=date_start)

### buy market ###

    def buy_asset_limit(self, quantity, symbol, last_price):
        try:
            buy_limit = self._client.order_limit_buy(symbol=symbol, quantity=quantity,
                                                     price=last_price)
            return buy_limit

        except BinanceAPIException as e:
            # error handling goes here
            print(e)
        except BinanceOrderException as e:
            # error handling goes here
            print(e)

    def buy_asset_market(self, quantity, symbol):
        try:
            buy_order_market = self._client.order_market_buy(symbol=symbol,
                                                             quantity=quantity)
            return buy_order_market

        except BinanceAPIException as e:
            # error handling goes here
            print(e)
        except BinanceOrderException as e:
            # error handling goes here
            print(e)

### sell market ###

    def sell_asset_limit(self, quantity, symbol, last_price):
        try:
            sell_order_market = self._client.order_limit_sell(symbol=symbol,
                                                              quantity=quantity,
                                                              price=last_price)
            return sell_order_market

        except BinanceAPIException as e:
            # error handling goes here
            print(e)
        except BinanceOrderException as e:
            # error handling goes here
            print(e)

    def sell_asset_market(self, quantity, symbol):
        try:
            sell_order_market = self._client.order_market_sell(symbol=symbol,
                                                               quantity=quantity)
            return sell_order_market

        except BinanceAPIException as e:
            # error handling goes here
            print(e)
        except BinanceOrderException as e:
            # error handling goes here
            print(e)

    def stop_loss_asset_market(self, quantity, symbol, stopPrice):
        try:
            sell_order_market = self._client.create_order(symbol=symbol, side='SELL', type='STOP_LOSS', quantity=quantity, stopPrice=stopPrice)
            return sell_order_market

        except BinanceAPIException as e:
            # error handling goes here
            print(e)
        except BinanceOrderException as e:
            # error handling goes here
            print(e)

    def stop_loss_limit_asset_market(self, quantity, symbol, stopPrice, price):
        try:
            sell_order_market = self._client.create_order(symbol=symbol, side='SELL', type='STOP_LOSS_LIMIT', quantity=quantity, stopPrice=stopPrice, timeInForce='GTC', price=price)
            return sell_order_market

        except BinanceAPIException as e:
            # error handling goes here
            print(e)
        except BinanceOrderException as e:
            # error handling goes here
            print(e)

### manage order ###

    def cancel_order(self, symbol, order):
        cancel = self._client.cancel_order(symbol=symbol, orderId=order['orderId'])
        return cancel

    def get_order(self, symbol, order):
        return self._client.get_all_orders(symbol=symbol, orderId=order['orderId'])

### manage asset ###

    def get_info_asset(self, symbol):
        return self._client.get_symbol_info(symbol)

    def get_precision_asset(self, symbol):
        lot_size = ''
        price_filter = ''
        for filters in self.get_info_asset(symbol)['filters']:
            if filters['filterType'] == 'LOT_SIZE':
                lot_size = filters
            elif filters['filterType'] == 'PRICE_FILTER':
                price_filter = filters
        return [lot_size, price_filter]
