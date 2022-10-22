"""
--------------------  Revision History: ----------------------------------------
* 2022-10-22    -   Class Created, also implemented with stop loss
* 2022-10-22    -   Small bug solved  for choosing selling signal
--------------------------------------------------------------------------------
Version Number: 1.1 V

Description
Video: https://www.youtube.com/watch?v=AXc1YAsCduI&ab_channel=Algovibes
Article: https://www.linkedin.com/pulse/algorithmic-trading-mean-reversion-using-python-bryan-chen/

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


def getFormattedSeries(series):
    index_name = []
    for i in range(len(series)):
        # reformat index
        index_name.append("Return for Trade " + str(i) + ": ")
        # reformat value
        series.iloc[i] = str(round(series.iloc[i] * 100, 2)) + " %"

    series.index = index_name
    return series


class MeanReversion(Strategy):
    df = pd.DataFrame()
    COLUMN_LIST = ['Date', 'Close']
    _buydates = []
    _selldates = []
    _buyprices = []
    _sellprices = []

    def __init__(self, ticker, interval, columns, lookbackHours='-1', startDate='noStartDate', endDate='noEndDate'):
        super(MeanReversion, self).__init__(ticker, interval, lookbackHours, startDate, endDate)
        # clean the dataframe adn set values for column
        self._calculateValuesForDf(columns)
        # print(self.df.tail(50))

    # calculate sma, std upper and lower band and signal and clear na:

    def plot(self):
        plt.figure(figsize=(23, 6))
        # plt.plot(self.df[['Close', 'SMA_20', 'upper_band', 'lower_band']])
        plt.plot(self.df[['Close']])
        plt.scatter(self.df.loc[self._buydates].index, self.df.loc[self._buydates].Close, marker='^', c='y')
        plt.scatter(self.df.loc[self._selldates].index, self.df.loc[self._selldates].Close, marker='v', c='g')
        # plt.fill_between(self.df.index, self.df.upper_band, self.df.lower_band, color='grey', alpha=0.8)
        # plt.legend(['Close', 'SMA_20', 'upper_band', 'lower_band'])
        plt.show()

    def backTest(self):
        # calculate relative return for each trade
        relative_returns = pd.Series(
            [(self._sellprices - self._buyprices) / self._buyprices for self._sellprices, self._buyprices
             in zip(self._sellprices, self._buyprices)])
        print(getFormattedSeries(relative_returns.copy()))
        cum_return = (relative_returns + 1).prod() - 1
        print("Cumulative returns: " + str(round(cum_return * 100, 2)) + " %")


    def _calculateValuesForDf(self, columns):
        column_len = len(columns)
        self.df = self.df.iloc[:, :column_len]
        self.df.columns = self.COLUMN_LIST
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
                self._buydates.append(index)
                self._buyprices.append(row.Close)
                position = True

            if position:
                if (row['signal'] == 'Sell') or (len(self._buyprices) != 0 and row['shifted_Close'] < 0.98 * self._buyprices[-1]):
                    self._selldates.append(index)
                    self._sellprices.append(row.Close)
                    position = False



# test the class
meanReversion = MeanReversion('BTCUSDT', '30m', MeanReversion.COLUMN_LIST, startDate='2022-08-01',
                              endDate=Strategy.today)
meanReversion.backTest()
meanReversion.plot()
