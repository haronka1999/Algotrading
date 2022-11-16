"""
--------------------  Revision History: ----------------------------------------
* 2022-10-15    -   Class Created
* 2022-10-21    -   Class getting first Version (1.0 V)
# 2022-10-22    -   Optimized code for Backtest.py
* 2022-11-16    -   Deleted default values for constructor's parameter list (it is handled in the UI side)
--------------------------------------------------------------------------------
Video: https://www.youtube.com/watch?v=8PzQSgw0SpM&t=915s
Description

Bollinger bands consist three bands:
Upper: SMA + 2*STD
Middle: SMA
Down: SMA -2*STD

This measure volatility but most importantly overbuying and overselling

and it should be used with other tech indicators

Buying strategy:
In this example we are selling when the upper trend is crossed, and we are buying when the down is crossed

Problem is you can have more buy signal than sell signal ( vice versa )
We handle this the following way:

    - we open in the first buying signal and ignore the other
    - we close in the first selling signal and ignore the other

Notes:
    - this strategy does not work well on bear market
    - this strategy need improvement: risk management and handle unclosed positions!
    - this is only 1 interpretation
-----------------------------------------------------------------------------------
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from strategies.Strategy import Strategy


# this price is equal with the percent of each trade
def calculateProfit(merged):
    return (merged.shift(-1)['Sell Price'] - merged['Buy Price']) / merged['Buy Price'] * 100


class BollingerBand(Strategy):
    ticker = ""
    interval = ""
    df = pd.DataFrame()
    COLUMN_LIST = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']

    def __init__(self, ticker, interval, columns, lookbackHours, startDate, endDate):
        super(BollingerBand, self).__init__(ticker, interval, columns, lookbackHours, startDate, endDate)
        # clean the dataframe adn set values for column
        self._calculateValuesForDf(columns)

    # calculate sma, std upper and lower band and signal and clear na:
    def _calculateValuesForDf(self, columns):
        self.df = self.df.set_index(self.COLUMN_LIST[0])
        self.df['STD'] = self.df.Close.rolling(window=20).std()
        self.df['SMA'] = self.df.Close.rolling(window=20).mean()
        self.df['upper'] = self.df.SMA + 2 * self.df.STD
        self.df['lower'] = self.df.SMA - 2 * self.df.STD

        self.df['Buy_Signal'] = np.where(self.df.lower > self.df.Close, True, False)
        self.df['Sell_Signal'] = np.where(self.df.upper < self.df.Close, True, False)
        self.chooseSignals()
        self.df = self.df.dropna()

    def chooseSignals(self):
        open_pos = False
        # getting only real trades loop through the df
        for i in range(len(self.df)):
            # buying pos
            if self.df.lower[i] > self.df.Close[i]:
                if not open_pos:
                    self.buydates.append(self.df.index[i])
                    self.buyprices.append(self.df.iloc[i].Close)
                    open_pos = True
            # selling pos
            elif self.df.upper[i] < self.df.Close[i]:
                if open_pos:
                    self.selldates.append(self.df.index[i])
                    self.sellprices.append(self.df.iloc[i].Close)
                    open_pos = False

    def plot(self):
        plt.figure(figsize=(25, 6))
        # plt.plot(self.df[['Close', 'SMA', 'upper', 'lower']])
        plt.plot(self.df[['Close']])
        # x-axis the time of buy_signal y Axis is the price at the price time
        plt.scatter(self.buydates, self.buyprices, marker='^', color='g')
        plt.scatter(self.selldates, self.sellprices, marker='^', color='y')
        # plt.fill_between(self.df.index, self.df.upper, self.df.lower, color='grey', alpha=0.3)
        plt.legend(['Close', 'SMA', 'upper', 'lower'])
        return plt

