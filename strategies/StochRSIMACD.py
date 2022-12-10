"""
--------------------  Revision History: ----------------------------------------
# 2022-11-11    -   Class created basic functionalities implemented
* 2022-11-16    -   Deleted default values for constructor's parameter list (it is handled in the UI side)
                    - class corrected  and got it's first form (not compatible with UI and Backtest yet
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
from matplotlib import pyplot as plt

from strategies.Strategy import Strategy
import numpy as np
import pandas as pd
import ta
from ta import momentum, trend

# backtest should have:
#   - sell and buy signals
#
# strategy should have
#   - a logi behind it
class StochRSIMACD(Strategy):
    def __init__(self, ticker, interval, lookback_time, startDate, endDate, api_key="", api_secret=""):
        super(StochRSIMACD, self).__init__(ticker, interval, lookback_time, startDate, endDate, api_key,
                                           api_secret)
        # clean the dataframe and set values for column
        self.actual_trades = None
        self._calculateValuesForDf()

    def _calculateValuesForDf(self):
        self._applyTechnicals()
        self.decide()

    def getBuyDatesForTradingBot(self):
        # print("actual trades: ")
        # print(self.actual_trades)
        return self.df.loc[self.actual_trades["Buying_dates"]]

    def getTrigger(self, lags, buy=True):
        dfx = pd.DataFrame()
        for i in range(lags + 1):
            if buy:
                mask = (self.df['%K'].shift(i) < 20) & (self.df['%D'].shift(i) < 20)
            else:
                mask = (self.df['%K'].shift(i) > 80) & (self.df['%D'].shift(i) > 80)
            dfx = pd.concat([dfx, pd.DataFrame([mask])], ignore_index=True)
            # dfx = dfx.append(mask, ignore_index=True)
        return dfx.sum(axis=0)

    # check if the trigger is fulfilled and buying condition fulfilled
    def decide(self):
        self.df['Buytrigger'] = np.where(self.getTrigger(20), 1, 0)
        self.df['Selltrigger'] = np.where(self.getTrigger(20, False), 1, 0)

        self.df['Buy'] = np.where(
            (self.df['Buytrigger']) & (self.df['%K'].between(20, 80)) & (self.df['%D'].between(20, 80)) & (
                    self.df.rsi > 50) & (self.df.macd > 0), 1, 0)

        self.df['Sell'] = np.where(
            (self.df['Selltrigger']) & (self.df['%K'].between(20, 80)) & (self.df['%D'].between(20, 80)) & (
                    self.df.rsi < 50) & (self.df.macd < 0), 1, 0)

        # Buying_dates, Selling_dates = [], []
        for i in range(len(self.df) - 1):
            # if my buying column contains a signal
            if self.df.Buy.iloc[i]:
                self.buydates.append(self.df.iloc[i + 1].name)
                # newDf = pd.DataFrame([self.df.iloc[i + 1].name])
                # self.buydates = pd.concat([self.buydates, newDf])
                # when I have appended a date I'm checking when my selling date is fulfilled
                # num =  number of iteration
                # j = the value of the Sell column in the numth iteration
                for num, j in enumerate(self.df.Sell[i:]):
                    if j:
                        self.selldates.append(self.df.iloc[i + num + 1].name)
                        # newDf = pd.DataFrame([self.df.iloc[i + num + 1].name])
                        # self.selldates = pd.concat([self.selldates, newDf])
                        break

        # if I have one extra buying date
        cut = len(self.buydates) - len(self.selldates)
        if cut:
            self.buydates = self.buydates[:-cut]
        frame = pd.DataFrame({'Buying_dates': self.buydates, 'Selling_dates': self.selldates})

        # avoid parallel trades we have to cut overlapping trades
        self.actual_trades = frame[frame.Buying_dates > frame.Selling_dates.shift(1)]

    def _applyTechnicals(self):
        self.df['%K'] = ta.momentum.stoch(self.df.High, self.df.Low, self.df.Close, window=14, smooth_window=3)
        self.df['%D'] = self.df['%K'].rolling(3).mean()
        self.df['rsi'] = ta.momentum.rsi(self.df.Close, window=14)
        self.df['macd'] = ta.trend.macd_diff(self.df.Close)
        # self.df.dropna(inplace=True)

    def plot(self):
        plt.figure(figsize=(20, 10))
        plt.plot(self.df.Close, color='k', alpha=0.7)
        plt.scatter(self.actual_trades.Buying_dates, self.df.Open[self.actual_trades.Buying_dates], marker='^',
                    color='g', s=500)
        plt.scatter(self.actual_trades.Selling_dates, self.df.Open[self.actual_trades.Selling_dates], marker='v',
                    color='r', s=500)
        plt.show()


# hej = StochRSIMACD('BTCUSDT', '5m', constants.COLUMN_LIST, '240', 'noStartDate', 'noEndDate')
# hej.plot()

hej = StochRSIMACD('BTCUSDT', '1m', '10 min', 'noStartDate', 'noEndDate', api_key="public",
                   api_secret="private")
