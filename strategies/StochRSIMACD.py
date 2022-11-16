"""
--------------------  Revision History: ----------------------------------------
# 2022-11-11    -   Class created basic functionalities implemented
* 2022-11-16    -   Deleted default values for constructor's parameter list (it is handled in the UI side)
--------------------------------------------------------------------------------
Video: https://www.youtube.com/watch?v=r8pU-8l1KPU
Description:
Indicators used:
    - %d = stochastic slow
    - %k = k line
    - RSI and MACD

Buying conditions:
    - %d and %k should be between 20-80
    - RSI >  50
    - MACD cross the signal line (must be the difference positive)

Selling Condition:
    - k and d lines above 20 and below 80
    - after the kand d line above 80
    - RSI < 50
    - signal line should cross the MACD line
---------------------------------------------------------------------------
"""

from strategies.Strategy import Strategy
import numpy as np
import pandas as pd
import ta
from ta import momentum, trend

from utils.Utilities import today

# TODO: Finish video and correct mistakes
class StochRSIMACD(Strategy):
    df = pd.DataFrame()
    COLUMN_LIST = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']

    def __init__(self, ticker, interval, columns, lookbackHours, startDate, endDate):
        super(StochRSIMACD, self).__init__(ticker, interval, columns, lookbackHours, startDate, endDate)
        # clean the dataframe and set values for column
        self._calculateValuesForDf(columns)
        print(self.df)

    def _calculateValuesForDf(self, columns):
        self.df = self.df.set_index(self.COLUMN_LIST[0])
        # k line
        self.df['%K'] = ta.momentum.stoch(self.df.High, self.df.Low, self.df.Close, window=14, smooth_window=3)
        # d line - stochastic slow = 3 period simple moving period
        self.df['%D'] = self.df['%K'].rolling(3).mean()
        self.df['rsi'] = ta.momentum.rsi(self.df.Close, window=14)
        self.df['macd'] = ta.trend.macd_diff(self.df.Close)
        self.df.dropna(inplace=True)

        self.df['Buytrigger'] = np.where(self.getTriggers(5, buy=True), 1, 0)
        self.df['Selltrigger'] = np.where(self.getTriggers(5, buy=False), 1, 0)
        self.df['Buy'] = np.where(
            self.df.Buytrigger & self.df['%K'].between(20, 80) & (self.df['%D'].between(20, 80)) & (
                        self.df.rsi > 50) & (self.df.macd > 0), 1,
            0)
        self.df['Sell'] = np.where(
            self.df.Selltrigger & self.df['%K'].between(20, 80) & (self.df['%D'].between(20, 80)) & (
                        self.df.rsi < 50) & (self.df.macd < 0), 1,
            0)

        self.filterValidSignals()

    def filterValidSignals(self):
        Buying_dates, Selling_dates = [], []
        for i in range(len(self.df) - 1):
            # check if BUying column contains a buy signal
            if self.df.Buy.iloc[i]:
                # we just can buy in the next timestap not in that one where we are  doing calculations
                Buying_dates.append(self.df.iloc[i + 1].name)
                # Buying_dates = pd.concat([Buying_dates, self.df.iloc[i + 1].name])
                # going only from the buying date ( this is only backtersting in real life is not possible)
                # j is 1 or 0
                # num: number of iteration
                for num, j in enumerate(self.df.Sell[i:]):
                    if j:
                        # Selling_dates.append(self.df.iloc[i + num + 1].name)
                        Selling_dates = pd.concat([Selling_dates, self.df.iloc[i + num + 1].name])
                        # only one selling
                        break

        # if we have buying dates and we have not selling dates
        cutit = len(Buying_dates) - len(Selling_dates)
        # calculate the more buying
        if cutit:
            Buying_dates = Buying_dates[:-cutit]

        print(len(Buying_dates))
        print(len(Selling_dates))
        frame = pd.DataFrame({'Buying_dates': Buying_dates, 'Selling_dates': Selling_dates})
        # delete those lines where there are multiple buying or selling signals
        actuals = frame[frame.Buying_dates > frame.Selling_dates.shift(1)]

    # having the line shifted back and checking if it's 20 and we need to repeat this line over and over for the days (1,2,3,4,...)
    # np.where((df['%K'].shift(1) < 20) & (df['%D'].shift(1) < 20) | (df['%K'].shift(2) < 20) & (df['%D'].shift(2) < 20))
    def getTriggers(self, lags, buy=True):
        dfx = pd.DataFrame()
        for i in range(1, lags + 1):
            if buy:
                # i it will be true if the crossing below twenty occured
                mask = (self.df['%K'].shift(i) < 20) & (self.df['%D'].shift(i) < 20)
                mask = mask * 1
            else:
                mask = (self.df['%K'].shift(i) > 80) & (self.df['%D'].shift(i) > 80)
            dfx = pd.concat([dfx, mask], ignore_index=True)
            # dfx = dfx.append(mask, ignore_index=True)
        return dfx.sum(axis=0)

    def plot(self):
        pass


strat = StochRSIMACD('BTCUSDT', '30m', StochRSIMACD.COLUMN_LIST, startDate='2021-01-01', endDate='2021-03-01')
