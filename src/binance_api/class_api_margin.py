from src.binance_api.class_api_spot import API
from binance.exceptions import BinanceAPIException, BinanceOrderException


class APIMargin(API):

    def __init__(self, api_key, api_secret):
        super().__init__(api_key, api_secret)

    ### manage account, asset and order ###

    def cancel_margin_order(self, symbol, order):
        cancel = self._client.cancel_margin_order(symbol=symbol, orderId=order['orderId'], isIsolated=True)
        return cancel

    def get_margin_account(self):
        return self._client.get_isolated_margin_account()

    def get_isolated_margin_info(self, symbol):
        return self._client.get_isolated_margin_account(symbol=symbol)

    def get_order(self, symbol, order):
        return self._client.get_margin_order(symbol=symbol, orderId=order['orderId'], isIsolated=True)

    def get_margin_all_orders(self, symbol):
        return self._client.get_all_margin_orders(symbol=symbol, IsIsolated=True)

    ### buy and sell with leverage ###

    def buy_margin_market_asset_leverage(self, symbol, quantity, leverage=1):
        #try:
        buy_order_market = self._client.create_margin_order(symbol=symbol, isIsolated=True, side="BUY",
                                                            type="MARKET", quantity=quantity * leverage,
                                                            sideEffectType="MARGIN_BUY")
        return buy_order_market

        # except BinanceAPIException as e:
        #     # error handling goes here
        #     print(e)
        # except BinanceOrderException as e:
        #     # error handling goes here
        #     print(e)

    def sell_margin_market_asset_repay(self, symbol, quantity):
        try:
            buy_order_market = self._client.create_margin_order(symbol=symbol, isIsolated=True, side="SELL",
                                                                type="MARKET", quantity=quantity,
                                                                sideEffectType="AUTO_REPAY")
            return buy_order_market

        except BinanceAPIException as e:
            # error handling goes here
            print(e)
        except BinanceOrderException as e:
            # error handling goes here
            print(e)

    def stop_loss_limit_margin_asset_market_repay(self, quantity, symbol, stopPrice, price):
        try:
            sell_order_market = self._client.create_margin_order(symbol=symbol, side='SELL', type='STOP_LOSS_LIMIT',
                                                                 quantity=quantity, stopPrice=stopPrice,
                                                                 timeInForce='GTC', price=price, isIsolated=True,
                                                                 sideEffectType="AUTO_REPAY")
            return sell_order_market

        except BinanceAPIException as e:
            # error handling goes here
            print(e)
        except BinanceOrderException as e:
            # error handling goes here
            print(e)

    ### buy and sell with short ###

    def short_margin_market_asset(self, symbol, quantity, leverage=1):
        # try:
        buy_order_market = self._client.create_margin_order(symbol=symbol, isIsolated=True, side="SELL",
                                                            type="MARKET", quantity=quantity * leverage,
                                                            sideEffectType="MARGIN_BUY")
        return buy_order_market

        # except BinanceAPIException as e:
        #     # error handling goes here
        #     print(e)
        # except BinanceOrderException as e:
        #     # error handling goes here
        #     print(e)

    def repay_short_margin_market_asset(self, symbol, quantity):
        try:
            buy_order_market = self._client.create_margin_order(symbol=symbol, isIsolated=True, side="BUY",
                                                                type="MARKET", quantity=quantity,
                                                                sideEffectType="AUTO_REPAY")
            return buy_order_market

        except BinanceAPIException as e:
            # error handling goes here
            print(e)
        except BinanceOrderException as e:
            # error handling goes here
            print(e)

    def stop_loss_short_limit_margin_asset_market_repay(self, quantity, symbol, stopPrice, price):
        try:
            sell_order_market = self._client.create_margin_order(symbol=symbol, side='BUY', type='STOP_LOSS_LIMIT',
                                                                 quantity=quantity, stopPrice=stopPrice,
                                                                 timeInForce='GTC', price=price, isIsolated=True,
                                                                 sideEffectType="AUTO_REPAY")
            return sell_order_market

        except BinanceAPIException as e:
            # error handling goes here
            print(e)
        except BinanceOrderException as e:
            # error handling goes here
            print(e)
