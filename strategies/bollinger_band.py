import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from strategies.strategy import Strategy
from utils.constants import Constants


class BollingerBand(Strategy):
    """
    Video: https://www.youtube.com/watch?v=8PzQSgw0SpM&t=915s
    Description

    Bollinger bands consist three bands:
    Upper: SMA + 2*STD
    Middle: SMA
    Down: SMA -2*STD

    Note:
        - measure only volatility but most importantly overbuying and overselling
        - it should be used with other tech indicators

    Buy signal
        - when Close price is below the lower band
    Sell signal:
         - when Close price is abowe the higher band

    Problem is you can have more buy signal than sell signal ( vice versa )
    We handle this the following way:

        - we open in the first buying signal and ignore the other
        - we close in the first selling signal and ignore the other

    Notes:
        - this strategy does not work well on bear market
        - this strategy need improvement: risk management and handle unclosed positions!
        - this is only 1 interpretation
    """
    def __init__(self, ticker, interval, lookback_time, start_date, end_date, api_key="", api_secret=""):
        super(BollingerBand, self).__init__(ticker, interval, lookback_time, start_date, end_date, api_key, api_secret)
        # clean the dataframe adn set values for column
        self.calculate_values_for_df()
        self.actual_trades = pd.DataFrame({
            'Buy Dates': self.buydates,
            'Buy Price': self.buyprices,
            'Sell Date': self.selldates,
            'Sell Price': self.sellprices
        })

    # calculate sma, std upper and lower band and signal and clear na:
    def calculate_values_for_df(self):
        self.df['STD'] = self.df.Close.rolling(window=20).std()
        self.df['SMA'] = self.df.Close.rolling(window=20).mean()
        self.df['upper'] = self.df.SMA + 2 * self.df.STD
        self.df['lower'] = self.df.SMA - 2 * self.df.STD
        # initilize only for zeros, later we will assign to the valid places
        self.df['Buy'] = 0
        self.df['Sell'] = 0
        self.choose_signals()
        self.df = self.df.dropna()


    def choose_signals(self):
        """
        We make sure that the strategy will not use overlapping signals,so we have to filter out
        :return: -
        """
        open_pos = False
        # getting only real trades loop through the df
        for i in range(len(self.df)):
            # buying pos
            if self.df.lower[i] > self.df.Close[i]:
                if not open_pos:
                    self.buydates.append(self.df.index[i])
                    self.buyprices.append(self.df.iloc[i].Close)
                    self.df["Buy"].iloc[i] = 1
                    open_pos = True
            # selling pos
            elif self.df.upper[i] < self.df.Close[i]:
                if open_pos:
                    self.selldates.append(self.df.index[i])
                    self.sellprices.append(self.df.iloc[i].Close)
                    self.df["Sell"].iloc[i] = 1
                    open_pos = False

        cut = len(self.buydates) - len(self.selldates)
        if cut:
            self.buydates = self.buydates[:-cut]
            self.buyprices = self.buyprices[:-cut]


    def plot(self):
        plt.figure(figsize=(25, 6))
        # plt.plot(self.df[['Close', 'SMA', 'upper', 'lower']])
        plt.plot(self.df[['Close']])
        # x-axis the time of buy_signal y Axis is the price at the price time
        plt.scatter(self.buydates, self.buyprices, marker='^', color='g', s=Constants.MARKER_SIZE)
        plt.scatter(self.selldates, self.sellprices, marker='^', color='y', s=Constants.MARKER_SIZE)
        # plt.fill_between(self.df.index, self.df.upper, self.df.lower, color='grey', alpha=0.3)
        plt.legend(['Close', 'SMA', 'upper', 'lower'])
        return plt
