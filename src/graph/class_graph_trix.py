import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import os


class CreateGraphTrix:
    width = {"1d": 0.9, "1h": 0.03, "4h": 0.1, "6h": 0.2, "1m": 0.001}

    @staticmethod
    def plot_trix_entry_exit(data, symbol, path):

        df = data.copy()
        # we plot our data
        df["date"] = df.index
        df["date"] = mpl_dates.date2num(df["date"])

        # we create the figure
        fig, ax = plt.subplots(3, 1, sharex='col', figsize=(10, 8),
                                       tight_layout=True, gridspec_kw={'height_ratios': [2, 1, 1]})

        # first the price
        ax[0].plot(df['close'])
        ax[0].scatter(df.index, df['buy'], color='green', label='Buy', marker='^', s=100)
        ax[0].scatter(df.index, df['sell'], color='red', label='Sell', marker='v', s=100)
        ax[0].legend()
        ax[0].set_ylabel('Close Price')

        date_format = mpl_dates.DateFormatter('%d-%m-%Y')
        ax[0].xaxis.set_major_formatter(date_format)
        fig.autofmt_xdate()
        plt.xlabel('Date')

        # secondly the trix
        ax[1].plot(df.index, df['TRIX_SIGNAL'], label="SMA of pct", c="orange")
        ax[1].plot(df.index, df['TRIX_PCT'], label="Percentage change of trix", c="green")
        ax[1].axhline(0, ls='--', c='black')
        ax[1].set_ylabel("Percentage of trix")
        ax[1].legend()

        # Stoch rsi
        ax[2].plot(df.index, df['STOCH_RSI']*100, c="purple")
        plt.axhline(80, ls='--', c='black')
        plt.axhline(20, ls='--', c='black')
        ax[2].set_ylabel("Stochastic RSI")
        ax[2].text(0, 0.82, "overbought", size=12, transform=ax[2].transAxes)
        ax[2].text(0, 0.11, "oversold", size=12, transform=ax[2].transAxes)

        plt.suptitle("Entry/exit for {}".format(symbol), size=20)
        if not os.path.exists(path + "{}/".format(symbol)):
            os.mkdir(path + "{}/".format(symbol))
        plt.savefig(path + "{}/Entry-exit-{}".format(symbol, symbol))
        plt.close('all')