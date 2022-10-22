"""
--------------------  Revision History: ----------------------------------------
* 2022-10-15    -   Class Created
* 2022-10-21    -  Class getting first Version (1.0 V)
--------------------------------------------------------------------------------
Version Number: 1.0 V

Description
Video: https://www.youtube.com/watch?v=8PzQSgw0SpM&t=915s

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

    def __init__(self, ticker, interval, columns, lookbackHours='-1', startDate='noStartDate', endDate='noEndDate'):
        super(BollingerBand, self).__init__(ticker, interval, lookbackHours, startDate, endDate)
        # clean the dataframe adn set values for column
        self._calculateValuesForDf(columns)

    # calculate sma, std upper and lower band and signal and clear na:
    def _calculateValuesForDf(self, columns):
        column_len = len(columns)
        self.df = self.df.iloc[:, :column_len]
        self.df.columns = self.COLUMN_LIST
        self.df = self.df.set_index(self.COLUMN_LIST[0])
        self.df['STD'] = self.df.Close.rolling(window=20).std()
        self.df['SMA'] = self.df.Close.rolling(window=20).mean()
        self.df['upper'] = self.df.SMA + 2 * self.df.STD
        self.df['lower'] = self.df.SMA - 2 * self.df.STD

        self.df['Buy_Signal'] = np.where(self.df.lower > self.df.Close, True, False)
        self.df['Sell_Signal'] = np.where(self.df.upper < self.df.Close, True, False)

        self.df = self.df.dropna()

    def chooseSignals(self):
        buys = []
        sells = []
        open_pos = False

        # getting only real trades loop through the df
        for i in range(len(self.df)):
            # buying pos
            if self.df.lower[i] > self.df.Close[i]:
                if not open_pos:
                    buys.append(i)
                    open_pos = True
            # selling pos
            elif self.df.upper[i] < self.df.Close[i]:
                if open_pos:
                    sells.append(i)
                    open_pos = False

        return buys, sells

    def plot(self):
        plt.figure(figsize=(25, 6))
        plt.plot(self.df[['Close', 'SMA', 'upper', 'lower']])

        # make sure that we ignore multiple signals: we open in the first and close in the first ignore the others
        buys, sells = self.chooseSignals()

        # x-axis the time of buy_signal y Axis is the price at the price time
        plt.scatter(self.df.iloc[buys].index, self.df.iloc[buys].Close, marker='^', color='g')
        plt.scatter(self.df.iloc[sells].index, self.df.iloc[sells].Close, marker='^', color='y')
        plt.fill_between(self.df.index, self.df.upper, self.df.lower, color='grey', alpha=0.3)
        plt.legend(['Close', 'SMA', 'upper', 'lower'])
        plt.show()

    def backTest(self):
        buys, sells = self.chooseSignals()
        # concat: combine series into a df
        # the close prices of the price and the sells close prices
        merged = pd.concat([self.df.iloc[buys].Close, self.df.iloc[sells].Close], axis=1)
        merged.columns = ['Buy Price', 'Sell Price']
        profit = calculateProfit(merged)
        print(profit)

    # test the class


bollingerStrategy = BollingerBand('BTCUSDT', '30m', BollingerBand.COLUMN_LIST, lookbackHours='130  ')
bollingerStrategy.backTest()
