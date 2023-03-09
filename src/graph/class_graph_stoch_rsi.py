import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
from mplfinance.original_flavor import candlestick_ohlc
import os


class CreateGraphStochRSI:
    width = {"1d": 0.9, "1h": 0.03, "4h": 0.1, "6h": 0.2, "1m": 0.001}

    @staticmethod
    def plot_rsi(rsi, interval, symbol, path):

        data = rsi.copy()
        # we plot our data
        data["date"] = data.index
        data["date"] = mpl_dates.date2num(data["date"])

        # we create the figure
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex='col', figsize=(10, 8), gridspec_kw={'height_ratios': [2, 1]},
                                       tight_layout=True)

        # first the price
        candlestick_ohlc(ax1, data[['date', 'open', 'high', 'low', 'close']].values, width=CreateGraphStochRSI.width[interval])
        ax1.set_ylabel('Price')

        date_format = mpl_dates.DateFormatter('%d-%m-%Y')
        ax1.xaxis.set_major_formatter(date_format)
        fig.autofmt_xdate()
        plt.xlabel('Date')

        # secondly the rsi

        ax2.plot(data.index, data['rsi'], c='purple')
        plt.ylim(0, 100)
        plt.axhline(70, ls='--', c='black')
        plt.axhline(30, ls='--', c='black')
        ax2.set_ylabel("RSI")
        ax2.text(0, 0.72, "overbought", size=12, transform=ax2.transAxes)
        ax2.text(0, 0.21, "oversold", size=12, transform=ax2.transAxes)

        plt.suptitle("Data for {}".format(symbol), size=20)
        if not os.path.exists(path + "{}/".format(symbol)):
            os.mkdir(path + "{}/".format(symbol))
        plt.savefig(path + "{}/RSI-{}".format(symbol, symbol))
        plt.close('all')

    @staticmethod
    def plot_stochastic_rsi(data, interval, symbol, path):

        stochastic_rsi = data.copy()
        # we plot our data
        stochastic_rsi["date"] = stochastic_rsi.index
        stochastic_rsi["date"] = mpl_dates.date2num(stochastic_rsi["date"])

        # we create the figure
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex='col', figsize=(10, 8), gridspec_kw={'height_ratios': [2, 1]},
                                       tight_layout=True)

        # first the price
        candlestick_ohlc(ax1, stochastic_rsi[['date', 'open', 'high', 'low', 'close']].values,
                         width=CreateGraphStochRSI.width[interval])
        ax1.set_ylabel('Price')

        date_format = mpl_dates.DateFormatter('%d-%m-%Y')
        ax1.xaxis.set_major_formatter(date_format)
        fig.autofmt_xdate()
        plt.xlabel('Date')

        # secondly the stoch rsi
        ax2.plot(stochastic_rsi.index, stochastic_rsi['%K'], c='blue', label="%K line")
        ax2.plot(stochastic_rsi.index, stochastic_rsi['%D'], c='orange', label="%D line")
        plt.ylim(0, 100)
        plt.axhline(80, ls='--', c='black')
        plt.axhline(20, ls='--', c='black')
        ax2.set_ylabel("Stochastic RSI")
        ax2.text(0, 0.82, "overbought", size=12, transform=ax2.transAxes)
        ax2.text(0, 0.11, "oversold", size=12, transform=ax2.transAxes)

        plt.legend()
        plt.suptitle("Data for {}".format(symbol), size=20)
        if not os.path.exists(path + "{}/".format(symbol)):
            os.mkdir(path + "{}/".format(symbol))
        plt.savefig(path + "{}/Stochastic RSI-{}".format(symbol, symbol))
        plt.close('all')

    @staticmethod
    def plot_stochastic_rsi_entry_exit(data, interval, symbol, path):

        stochastic_rsi = data.copy()
        # we plot our data
        stochastic_rsi["date"] = stochastic_rsi.index
        stochastic_rsi["date"] = mpl_dates.date2num(stochastic_rsi["date"])

        # we create the figure
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex='col', figsize=(10, 8), gridspec_kw={'height_ratios': [2, 1]},
                                       tight_layout=True)

        # first the price
        ax1.plot(stochastic_rsi['close'])
        ax1.scatter(stochastic_rsi.index, stochastic_rsi['buy'], color='green', label='Buy', marker='^', s=100)
        ax1.scatter(stochastic_rsi.index, stochastic_rsi['sell'], color='red', label='Sell', marker='v', s=100)
        ax1.legend()
        ax1.set_ylabel('Close Price')

        date_format = mpl_dates.DateFormatter('%d-%m-%Y')
        ax1.xaxis.set_major_formatter(date_format)
        fig.autofmt_xdate()
        plt.xlabel('Date')

        # secondly the stoch rsi
        ax2.plot(stochastic_rsi.index, stochastic_rsi['%K'], c='blue', label="%K line")
        ax2.plot(stochastic_rsi.index, stochastic_rsi['%D'], c='orange', label="%D line")
        plt.ylim(0, 100)
        plt.axhline(80, ls='--', c='black')
        plt.axhline(20, ls='--', c='black')
        ax2.set_ylabel("Stochastic RSI")
        ax2.text(0, 0.82, "overbought", size=12, transform=ax2.transAxes)
        ax2.text(0, 0.11, "oversold", size=12, transform=ax2.transAxes)

        plt.legend()
        plt.suptitle("Entry/exit for {}".format(symbol), size=20)
        if not os.path.exists(path + "{}/".format(symbol)):
            os.mkdir(path + "{}/".format(symbol))
        plt.savefig(path + "{}/Entry-exit-{}".format(symbol, symbol))
        plt.close('all')
