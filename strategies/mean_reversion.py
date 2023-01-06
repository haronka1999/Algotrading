import numpy as np
import pandas as pd
from ta import momentum
from matplotlib import pyplot as plt
from strategies.strategy import Strategy
from utils.constants import Constants


class MeanReversion(Strategy):
    """
    Video: https://www.youtube.com/watch?v=AXc1YAsCduI&ab_channel=Algovibes
    Article: https://www.linkedin.com/pulse/algorithmic-trading-mean-reversion-using-python-bryan-chen/
    Description

    Strategy: if a stock is going up than we can sell and if it goes down it, we can buy

    Buy:  RSI < 30 and Lower bollinger band is crossed by the price
    Sell: RSI > 70 and Upper bollinger band is crossed by the price
    Stop Loss: We shift for the last value because we are buying in the current row, and we are taking the 95 %
        of the last buy price

    Notes:
        - it is good in sideways market
        - we can create stop loss, but it will cannot skip black - swan events, and it will
        decrease performance
    """
    def __init__(self, ticker, interval, lookback_time, start_date, end_date, api_key="", api_secret=""):
        self.df = pd.DataFrame()
        super(MeanReversion, self).__init__(ticker, interval, lookback_time, start_date, end_date, api_key, api_secret)
        # clean the dataframe adn set values for column
        self.calculate_values_for_df()
        self.actual_trades = pd.DataFrame({
            'Buy Date': self.buydates,
            'Buy Price': self.buyprices,
            'Sell Date': self.selldates,
            'Sell Price': self.sellprices
        })

    def calculate_values_for_df(self):
        self.df['SMA_20'] = self.df.Close.rolling(20).mean()
        #  rolling standard deviation (vol = volatility )
        self.df['vol'] = self.df.Close.rolling(20).std()
        self.df['upper_band'] = self.df['SMA_20'] + (2 * self.df['vol'])
        self.df['lower_band'] = self.df['SMA_20'] - (2 * self.df['vol'])
        self.df['rsi'] = momentum.rsi(self.df.Close, window=6)

        # check conditions
        self.df['Buy'] = np.where((self.df.rsi < 30) & (self.df.Close < self.df['lower_band']), 1, 0)
        self.df['Sell'] = np.where((self.df.rsi > 70) & (self.df.Close > self.df['upper_band']), 1, 0)
        self.df = self.df.dropna()

        # this is for the stop loss (we get the one row before)
        self.df['shifted_Close'] = self.df.Close.shift()
        self.get_signals()


    # loop over the rows screen for buys set a position flag (we do not buy again)
    # sell if we are in a position
    def get_signals(self):
        # default shift is 1
        self.df.Buy, self.df.Sell = self.df.Buy.shift(), self.df.Sell.shift()
        position = False

        for index, row in self.df.iterrows():
            if not position and row['Buy'] == 1:
                self.buydates.append(index)
                self.buyprices.append(row.Close)
                position = True

            if position:
                if (row['Sell'] == 1) or (
                        len(self.buyprices) != 0 and row['shifted_Close'] < 0.98 * self.buyprices[-1]):
                    self.selldates.append(index)
                    self.sellprices.append(row.Close)
                    position = False

        # if I have one extra buying date delete it
        cut = len(self.buydates) - len(self.selldates)
        if cut:
            self.buydates = self.buydates[:-cut]
            self.buyprices = self.buyprices[:-cut]


    def plot(self):
        plt.figure(figsize=(23, 6))
        # plt.plot(self.df[['Close', 'SMA_20', 'upper_band', 'lower_band']])
        plt.plot(self.df[['Close']])
        plt.scatter(self.df.loc[self.buydates].index, self.df.loc[self.buydates].Close, marker='^', c='y',
                    s=Constants.MARKER_SIZE)
        plt.scatter(self.df.loc[self.selldates].index, self.df.loc[self.selldates].Close, marker='v', c='g',
                    s=Constants.MARKER_SIZE)
        return plt
        # plt.fill_between(self.df.index, self.df.upper_band, self.df.lower_band, color='grey', alpha=0.8)
        # plt.legend(['Close', 'SMA_20', 'upper_band', 'lower_band'])
        # plt.show()
