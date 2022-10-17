# Read the docs below for understanding
'''
A demonstration of pure Ballinger Band
Ballling bands consist three bands:
Upper: SMA + 2*STD
Middle: SMA
Down: SMA -2*STD

This measure volatility but most importantly overbuying and overselling
More than 1 interpretation,
and it should be used with other tech indicators

Buying strategy:
In this example we are selling when the upper trend is crossed, and we are buying when the down is crossed

Problem is you can have more buy signal than sell signal ( vice versa )
We handle this the following way:

    we open in the first buying signal and ignore the other
    we close in the first selling signal and ignore the other

Note: this strategy does not work well on bear market
'''
import pdb
import sys

from dataScraping.GetHistoricalData import GetHistoricalData, validate, BOLLINGER_COLUMN_LIST
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from strategies.Strategy import Strategy


class BollingerBand(Strategy):
    ticker = ""
    interval = ""
    df = pd.DataFrame()

    def __init__(self, ticker, interval, columns, lookbackHours='-1', startDate='noStartDate', endDate='noEndDate'):
        self.ticker = ticker
        self.interval = interval

        if lookbackHours != -1:
            data = GetHistoricalData(ticker, interval, lookbackHours=lookbackHours)
        elif startDate != 'noStartDate' and endDate != 'noEndDate':
            validate(startDate)
            validate(endDate)
            data = GetHistoricalData(ticker, interval, startDate=startDate, endDate=endDate)
        else:
            print("something wron with the parameters please try again")
            sys.exit()
        self.df = data.getDataFrame()
        # clean the dataframe adn set values for column
        self.calculateValuesForDf(columns)

    # calculate sma, std upper and lower band and signal and clear na:
    def calculateValuesForDf(self, columns):
        column_len = len(columns)
        self.df = self.df.iloc[:, :column_len]
        self.df.columns = BOLLINGER_COLUMN_LIST
        self.df = self.df.set_index(BOLLINGER_COLUMN_LIST[0])
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
                    buys.append(self.df.Close[i])
                    open_pos = True
            # selling pos
            elif self.df.upper[i] < self.df.Close[i]:
                if open_pos:
                    sells.append(self.df.Close[i])
                    open_pos = False

        return buys,sells

    def plot(self):
        plt.figure(figsize=(25, 6))
        plt.plot(self.df[['Close', 'SMA', 'upper', 'lower']])

        # make sure that we ignore multiple signals: we open in the first and close in the first ignore the others
        buys, sells = self.chooseSignals()

        # x axis the time of buy_signal y Axis is the price at the price time
        # TODO: finish the video : https://www.youtube.com/watch?v=8PzQSgw0SpM
        # understand how these upper and lower conditions works (ergo: chooseSignals() function)
        # and  correct the plot as the video shows
        plt.scatter(self.df.index[self.df.Buy_Signal], self.df[self.df.Buy_Signal].Close, marker='^', color='g')
        plt.scatter(self.df.index[self.df.Sell_Signal], self.df[self.df.Sell_Signal].Close, marker='^', color='y')
        plt.fill_between(self.df.index, self.df.upper, self.df.lower, color='grey', alpha=0.3)
        plt.legend(['Close', 'SMA', 'upper', 'lower'])
        plt.show()



#test the class
bollingerStrategy = BollingerBand('BTCUSDT', '30m', BOLLINGER_COLUMN_LIST, lookbackHours='96')
bollingerStrategy.plot()


