from matplotlib import pyplot as plt
from strategies.strategy import Strategy
import numpy as np
import pandas as pd
import ta
from ta import momentum, trend
from utils.constants import Constants


class StochRSIMACD(Strategy):
    """
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
    """

    def __init__(self, ticker, interval, lookback_time, start_date, end_date, api_key="", api_secret=""):
        super(StochRSIMACD, self).__init__(ticker, interval, lookback_time, start_date, end_date, api_key,
                                           api_secret)
        # clean the dataframe and set values for column
        self.lags = 20
        self.actual_trades = pd.DataFrame()
        self.calculate_values_for_df()

    def calculate_values_for_df(self):
        self.apply_technicals()
        self.decide()


    # check if the trigger is fulfilled and buying condition fulfilled
    def decide(self):
        self.df['Buytrigger'] = np.where(self.get_trigger(self.lags), 1, 0)
        self.df['Selltrigger'] = np.where(self.get_trigger(self.lags, False), 1, 0)

        self.df['Buy'] = np.where(
            (self.df['Buytrigger']) & (self.df['%K'].between(20, 80)) & (self.df['%D'].between(20, 80)) & (
                    self.df.rsi > 50) & (self.df.macd > 0), 1, 0)

        self.df['Sell'] = np.where(
            (self.df['Selltrigger']) & (self.df['%K'].between(20, 80)) & (self.df['%D'].between(20, 80)) & (
                    self.df.rsi < 50) & (self.df.macd < 0), 1, 0)

        for i in range(len(self.df) - 1):
            # if my buying column contains a signal
            if self.df.Buy.iloc[i]:
                self.buydates.append(self.df.iloc[i + 1].name)
                # when I have appended a date I'm checking when my selling date is fulfilled
                # num =  number of iteration
                # j = the value of the Sell column in the numth iteration
                for num, j in enumerate(self.df.Sell[i:]):
                    if j:
                        self.selldates.append(self.df.iloc[i + num + 1].name)
                        break

        self.create_actual_trades()

        # if I have one extra buying date delete it
        cut = len(self.buydates) - len(self.selldates)
        if cut:
            self.buydates = self.buydates[:-cut]
            self.buyprices = self.buyprices[:-cut]

    def get_trigger(self, lags, buy=True):
        dfx = pd.DataFrame()
        for i in range(lags + 1):
            if buy:
                mask = (self.df['%K'].shift(i) < 20) & (self.df['%D'].shift(i) < 20)
            else:
                mask = (self.df['%K'].shift(i) > 80) & (self.df['%D'].shift(i) > 80)
            dfx = pd.concat([dfx, pd.DataFrame([mask])], ignore_index=True)
            # dfx = dfx.append(mask, ignore_index=True)
        return dfx.sum(axis=0)

    def apply_technicals(self):
        self.df['%K'] = ta.momentum.stoch(self.df.High, self.df.Low, self.df.Close, window=14, smooth_window=3)
        self.df['%D'] = self.df['%K'].rolling(3).mean()
        self.df['rsi'] = ta.momentum.rsi(self.df.Close, window=14)
        self.df['macd'] = ta.trend.macd_diff(self.df.Close)
        self.df.dropna(inplace=True)

    def plot(self):
        plt.figure(figsize=(20, 10))
        plt.plot(self.df.Close, color='k', alpha=0.7)

        plt.scatter(self.actual_trades['Buy Date'], self.actual_trades['Buy Price'], marker='^',
                    color='g', s=Constants.MARKER_SIZE)
        plt.scatter(self.actual_trades['Sell Date'], self.actual_trades['Sell Price'], marker='v',
                    color='r', s=Constants.MARKER_SIZE)
        return plt

    def create_actual_trades(self):
        temp_frame = pd.DataFrame(
            {'Buy Date': self.buydates, 'Sell Date': self.selldates})
        # avoid parallel trades we have to cut overlapping trades
        frame = temp_frame[temp_frame['Buy Date'] > temp_frame['Sell Date'].shift(1)]

        self.buydates = frame['Buy Date']
        self.buydates.reset_index(drop=True, inplace=True)
        self.selldates = frame['Sell Date']
        self.selldates.reset_index(drop=True, inplace=True)
        self.buyprices = self.df.Open[self.buydates]
        self.buyprices.reset_index(drop=True, inplace=True)
        self.sellprices = self.df.Open[self.selldates]
        self.sellprices.reset_index(drop=True, inplace=True)

        self.actual_trades = pd.DataFrame({
            'Buy Date': self.buydates,
            'Buy Price': self.buyprices,
            'Sell Date': self.selldates,
            'Sell Price': self.sellprices
        })
