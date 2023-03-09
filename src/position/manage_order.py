from math import *
from src.position.class_time import Time


class ManageOrder:

    @staticmethod
    def buy_margin_with_sl(api, symbol, quantity, leverage, stop_loss, quantity_precision, price_precision, path):
        buy_market_order = api.buy_margin_market_asset_leverage(symbol=symbol, quantity=quantity,
                                                                leverage=leverage)
        Time.wait(1)
        commission_asset = sum(
            [float(buy_market_order['fills'][i]['commission']) for i in
             range(len(buy_market_order['fills']))])
        quantity_bought = floor(
            (float(buy_market_order['executedQty']) - commission_asset) * 10 ** quantity_precision) / (
                                  10 ** quantity_precision)
        usdt_borrow = float(buy_market_order['marginBuyBorrowAmount'])

        copy_order = buy_market_order
        del copy_order['clientOrderId'], copy_order['transactTime'], copy_order['orderId'], copy_order['timeInForce'], copy_order['isIsolated'], copy_order['status'], copy_order['type']

        with open(path + "{}/trade-{}.txt".format(symbol, symbol), "a") as f:
            f.write("Buy order : \n")
            f.write(str(copy_order) + "\n")

        # Stop loss
        stopPrice = round(float(buy_market_order['fills'][0]['price']) * (1 - stop_loss / 100),
                          price_precision)
        price = round(
            float(buy_market_order['fills'][0]['price']) * (1 - stop_loss / 100 - 0.001),
            price_precision)
        stop_loss_limit = api.stop_loss_limit_margin_asset_market_repay(
            quantity=quantity_bought,
            symbol=symbol, stopPrice=stopPrice,
            price=price)

        Time.wait(2)
        stop_loss_limit = api.get_order(symbol=symbol, order=stop_loss_limit)
        copy_order = stop_loss_limit
        del copy_order['clientOrderId'], copy_order['executedQty'], copy_order['cummulativeQuoteQty'], copy_order['timeInForce'], copy_order['time'], copy_order['updateTime'], copy_order['accountId'], copy_order['isIsolated'], copy_order['icebergQty']

        with open(path + "{}/trade-{}.txt".format(symbol, symbol), "a") as f:
            f.write("Stop loss : \n")
            f.write(str(copy_order) + "\n")

        return buy_market_order, stop_loss_limit, quantity_bought, usdt_borrow

    @staticmethod
    def short_margin_with_sl(api, symbol, quantity, leverage, stop_loss, price_precision, path):
        sell_short_market_order = api.short_margin_market_asset(symbol, quantity=quantity,
                                                                leverage=leverage)
        Time.wait(2)
        quantity_sold = float(sell_short_market_order['executedQty'])

        copy_order = sell_short_market_order
        del copy_order['clientOrderId'], copy_order['transactTime'], copy_order['orderId'], copy_order['timeInForce'], copy_order['isIsolated'], copy_order['status'], copy_order['type']
        with open(path + "{}/trade-{}.txt".format(symbol, symbol), "a") as f:
            f.write("Short order : \n")
            f.write(str(copy_order) + "\n")

        # Stop loss
        stopPrice = round(
            float(sell_short_market_order['fills'][0]['price']) * (1 + stop_loss / 100),
            price_precision)
        price = round(
            float(sell_short_market_order['fills'][0]['price']) * (1 + stop_loss / 100 + 0.001),
            price_precision)
        short_stop_loss_limit = api.stop_loss_short_limit_margin_asset_market_repay(
            quantity=quantity_sold,
            symbol=symbol, stopPrice=stopPrice,
            price=price)
        Time.wait(2)
        short_stop_loss_limit = api.get_order(symbol=symbol,
                                                     order=short_stop_loss_limit)

        copy_order = short_stop_loss_limit
        del copy_order['clientOrderId'], copy_order['executedQty'], copy_order['cummulativeQuoteQty'], copy_order['timeInForce'], copy_order['time'], copy_order['updateTime'], copy_order['accountId'], copy_order['isIsolated'], copy_order['icebergQty']
        with open(path + "{}/trade-{}.txt".format(symbol, symbol), "a") as f:
            f.write("Stop loss : \n")
            f.write(str(copy_order) + "\n")
        return sell_short_market_order, short_stop_loss_limit, quantity_sold

    @staticmethod
    def sell_repay_margin(api, symbol, stop_loss_limit, buy_market_order, quantity_bought, usdt_borrow, update_usdt,
                          nb_usdt, profit, path):
        api.cancel_margin_order(symbol, stop_loss_limit)
        sell_market_order = api.sell_margin_market_asset_repay(quantity=quantity_bought,
                                                               symbol=symbol)
        if update_usdt:
            nb_usdt = float(sell_market_order['cummulativeQuoteQty']) - usdt_borrow
        else:
            profit.append(float(sell_market_order['cummulativeQuoteQty']) - float(
                buy_market_order['cummulativeQuoteQty']))

        copy_order = sell_market_order
        del copy_order['clientOrderId'], copy_order['transactTime'], copy_order['orderId'], copy_order['timeInForce'], copy_order['isIsolated'], copy_order['status'], copy_order['type']

        with open(path + "{}/trade-{}.txt".format(symbol, symbol), "a") as f:
            f.write("Sell order : \n")
            f.write(str(copy_order) + "\n")
            f.write("USDT value : \n")
            if update_usdt:
                f.write(str(nb_usdt) + " $ " + "remaining \n")
            else:
                f.write(str(sum(profit)) + " $ " + "profit \n")

        return nb_usdt, profit

    @staticmethod
    def buy_repay_margin(api, symbol, short_stop_loss_limit, sell_short_market_order, quantity_sold, update_usdt,
                         nb_usdt, profit, path):
        api.cancel_margin_order(symbol, short_stop_loss_limit)
        buy_short_market_order = api.repay_short_margin_market_asset(quantity=quantity_sold,
                                                                     symbol=symbol)
        if update_usdt:
            nb_usdt += float(sell_short_market_order['cummulativeQuoteQty']) - float(
                buy_short_market_order['cummulativeQuoteQty'])
        else:
            profit.append(float(sell_short_market_order['cummulativeQuoteQty']) - float(
                buy_short_market_order['cummulativeQuoteQty']))

        copy_order = buy_short_market_order
        del copy_order['clientOrderId'], copy_order['transactTime'], copy_order['orderId'], copy_order['timeInForce'], copy_order['isIsolated'], copy_order['status'], copy_order['type']
        with open(path + "{}/trade-{}.txt".format(symbol, symbol), "a") as f:
            f.write("Buy short order : \n")
            f.write(str(buy_short_market_order) + "\n")
            f.write("USDT value : \n")
            if update_usdt:
                f.write(str(nb_usdt) + " $ " + "remaining \n")
            else:
                f.write(str(sum(profit)) + " $ " + "profit \n")

        return nb_usdt, profit

    @staticmethod
    def stop_loss_executed(symbol, stop_loss_limit, buy_market_order, update_usdt, nb_usdt, usdt_borrow, profit, path):
        if update_usdt:
            nb_usdt = float(stop_loss_limit['cummulativeQuoteQty']) - usdt_borrow
        else:
            profit.append(float(stop_loss_limit['cummulativeQuoteQty']) - float(
                buy_market_order['cummulativeQuoteQty']))

        copy_order = stop_loss_limit
        del copy_order['clientOrderId'], copy_order['timeInForce'], copy_order['time'], copy_order['updateTime'], copy_order['accountId'], copy_order['isIsolated'], copy_order['icebergQty']
        with open(path + "{}/trade-{}.txt".format(symbol, symbol), "a") as f:
            f.write("stop loss has been performed \n")
            f.write(str(copy_order) + "\n")
            f.write("USDT value : \n")
            if update_usdt:
                f.write(str(nb_usdt) + " $ " + "remaining \n")
            else:
                f.write(str(sum(profit)) + " $ " + "profit \n")

        return nb_usdt, profit

    @staticmethod
    def short_stop_loss_executed(symbol, short_stop_loss_limit, sell_short_market_order, update_usdt, nb_usdt, profit, path):
        if update_usdt:
            nb_usdt += float(sell_short_market_order['cummulativeQuoteQty']) - float(
                short_stop_loss_limit['cummulativeQuoteQty'])
        else:
            profit.append(float(sell_short_market_order['cummulativeQuoteQty']) - float(
                short_stop_loss_limit['cummulativeQuoteQty']))

        copy_order = short_stop_loss_limit
        del copy_order['clientOrderId'], copy_order['timeInForce'], copy_order['time'], copy_order['updateTime'], copy_order['accountId'], copy_order['isIsolated'], copy_order['icebergQty']
        with open(path + "{}/trade-{}.txt".format(symbol, symbol), "a") as f:
            f.write("stop loss has been performed \n")
            f.write(str(copy_order) + "\n")
            f.write("USDT value : \n")
            if update_usdt:
                f.write(str(nb_usdt) + " $ " + "remaining \n")
            else:
                f.write(str(sum(profit)) + " $ " + "profit \n")

        return nb_usdt, profit
