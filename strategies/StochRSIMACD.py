"""
--------------------  Revision History: ----------------------------------------
# 2022-11-11    -   Class created basic functionalities implemented
* 2022-11-16    -   Deleted default values for constructor's parameter list (it is handled in the UI side)
                    - class corrected  and got it's first form (not compatible with UI and Backtest yet
--------------------------------------------------------------------------------
Video: https://www.youtube.com/watch?v=r8pU-8l1KPU and https://www.youtube.com/watch?v=X50-c54BWV8&t=53s
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
from matplotlib import pyplot as plt

from strategies.Strategy import Strategy
import numpy as np
import pandas as pd
import ta
from ta import momentum, trend

from utils import constants


class StochRSIMACD(Strategy):
    df = pd.DataFrame()
    COLUMN_LIST = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']

    def __init__(self, ticker, interval, columns, lookbackHours, startDate, endDate):
        super(StochRSIMACD, self).__init__(ticker, interval, columns, lookbackHours, startDate, endDate)
        # clean the dataframe and set values for column
        self.actual_trades = None
        self._calculateValuesForDf(columns)

        # print(self.df)

    def _calculateValuesForDf(self, columns):
        self.df = self.df.set_index(self.COLUMN_LIST[0])
        self._applyTechnicals()
        self.decide()

    def getTrigger(self, lags, buy=True):
        dfx = pd.DataFrame()
        for i in range(lags + 1):
            if buy:
                mask = (self.df['%K'].shift(i) < 20) & (self.df['%D'].shift(i) < 20)
            else:
                mask = (self.df['%K'].shift(i) > 80) & (self.df['%D'].shift(i) > 80)
            dfx = dfx.append(mask, ignore_index=True)
        return dfx.sum(axis=0)

    # check if the trigger is fulfilled and buying condition fulfilled
    def decide(self):
        self.df['Buytrigger'] = np.where(self.getTrigger(4), 1, 0)
        self.df['Selltrigger'] = np.where(self.getTrigger(4, False), 1, 0)

        self.df['Buy'] = np.where(
            (self.df['Buytrigger']) & (self.df['%K'].between(20, 80)) & (self.df['%D'].between(20, 80)) & (
                    self.df.rsi > 50) & (self.df.macd > 0), 1, 0)

        self.df['Sell'] = np.where(
            (self.df['Selltrigger']) & (self.df['%K'].between(20, 80)) & (self.df['%D'].between(20, 80)) & (
                    self.df.rsi < 50) & (self.df.macd < 0), 1, 0)

        Buying_dates, Selling_dates = [], []
        for i in range(len(self.df) - 1):
            # if my buying column contains a signal
            if self.df.Buy.iloc[i]:
                Buying_dates.append(self.df.iloc[i + 1].name)
                # when I have appended a date I'm checking when my selling date is fulfilled
                # num =  number of iteration
                # j = the value of the Sell column in the numth iteration
                for num, j in enumerate(self.df.Sell[i:]):
                    if j:
                        Selling_dates.append(self.df.iloc[i + num + 1].name)
                        break

        # if I have one extra buying date
        cut = len(Buying_dates) - len(Selling_dates)
        if cut:
            Buying_dates = Buying_dates[:-cut]
        frame = pd.DataFrame({'Buying_dates': Buying_dates, 'Selling_dates': Selling_dates})

        # avoid parallel trades we have to cut overlapping trades
        self.actual_trades = frame[frame.Buying_dates > frame.Selling_dates.shift(1)]
        print(self.actual_trades)
        BuyPrices = self.df.loc[self.actual_trades.Buying_dates].Open
        SellPrices = self.df.loc[self.actual_trades.Selling_dates].Open
        print(str((SellPrices.values - BuyPrices.values) / BuyPrices.values))

    def _applyTechnicals(self):
        self.df['%K'] = ta.momentum.stoch(self.df.High, self.df.Low, self.df.Close, window=14, smooth_window=3)
        self.df['%D'] = self.df['%K'].rolling(3).mean()
        self.df['rsi'] = ta.momentum.rsi(self.df.Close, window=14)
        self.df['macd'] = ta.trend.macd_diff(self.df.Close)
        self.df.dropna(inplace=True)

    def plot(self):
        plt.figure(figsize=(20, 10))
        plt.plot(self.df.Close, color='k', alpha=0.7)
        plt.scatter(self.actual_trades.Buying_dates, self.df.Open[self.actual_trades.Buying_dates], marker='^',
                    color='g', s=500)
        plt.scatter(self.actual_trades.Selling_dates, self.df.Open[self.actual_trades.Selling_dates], marker='v',
                    color='r', s=500)
        plt.show()


hej = StochRSIMACD('BTCUSDT', '5m', constants.COLUMN_LIST, '240', 'noStartDate', 'noEndDate')
hej.plot()
