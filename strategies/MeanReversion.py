"""
--------------------  Revision History: ----------------------------------------
* 2022-10-22    -   Class Created, also implemented with stop loss
* 2022-10-22    -   Small bug solved  for choosing selling signal
* 2022-10-22    -   Optimized for Backtest.py class
* 2022-11-16    -   Deleted default values for constructor's parameter list (it is handled in the UI side)
--------------------------------------------------------------------------------
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
-----------------------------------------------------------------------------------
"""

import numpy as np
import pandas as pd
from ta import momentum
from matplotlib import pyplot as plt
from strategies.Strategy import Strategy


class MeanReversion(Strategy):

    COLUMN_LIST = ['Date', 'Close']


    def __init__(self, ticker, interval, columns, lookbackHours, startDate, endDate):
        self.df = pd.DataFrame()
        super(MeanReversion, self).__init__(ticker, interval,columns, lookbackHours, startDate, endDate)
        # clean the dataframe adn set values for column
        self._calculateValuesForDf(columns)

    def plot(self):
        plt.figure(figsize=(23, 6))
        # plt.plot(self.df[['Close', 'SMA_20', 'upper_band', 'lower_band']])
        plt.plot(self.df[['Close']])
        plt.scatter(self.df.loc[self.buydates].index, self.df.loc[self.buydates].Close, marker='^', c='y')
        plt.scatter(self.df.loc[self.selldates].index, self.df.loc[self.selldates].Close, marker='v', c='g')
        # plt.fill_between(self.df.index, self.df.upper_band, self.df.lower_band, color='grey', alpha=0.8)
        # plt.legend(['Close', 'SMA_20', 'upper_band', 'lower_band'])
        plt.show()

    def get_sellprices(self):
        return self.sellprices

    def get_buyprices(self):
        return self.buyprices

    def _calculateValuesForDf(self, columns):
        self.df = self.df.set_index(self.COLUMN_LIST[0])
        self.df['SMA_20'] = self.df.Close.rolling(20).mean()
        #  rolling standard deviation (vol = volatility )
        self.df['vol'] = self.df.Close.rolling(20).std()
        self.df['upper_band'] = self.df['SMA_20'] + (2 * self.df['vol'])
        self.df['lower_band'] = self.df['SMA_20'] - (2 * self.df['vol'])
        self.df['rsi'] = momentum.rsi(self.df.Close, window=6)

        conditions = [(self.df.rsi < 30) & (self.df.Close < self.df['lower_band']),
                      (self.df.rsi > 70) & (self.df.Close > self.df.upper_band)]
        choices = ['Buy', 'Sell']
        self.df['signal'] = np.select(conditions, choices)
        self.df = self.df.dropna()

        # this is for the stop loss (we get the one row before)
        self.df['shifted_Close'] = self.df.Close.shift()
        self._getSignals()

    # loop over the rows screen for buys set a position flag (we do not buy again)
    # sell if we are in a position
    def _getSignals(self):
        # default shift is 1
        self.df.signal = self.df.signal.shift()
        position = False

        for index, row in self.df.iterrows():
            if not position and row['signal'] == 'Buy':
                self.buydates.append(index)
                self.buyprices.append(row.Close)
                position = True

            if position:
                if (row['signal'] == 'Sell') or (len(self.buyprices) != 0 and row['shifted_Close'] < 0.98 * self.buyprices[-1]):
                    self.selldates.append(index)
                    self.sellprices.append(row.Close)
                    position = False
