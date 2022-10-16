# Read the docs below for understanding
'''
A demonstration of pure Ballinger Band
Ballling bands consist three bands:
Upper: SMA + 2*STD
Middle: SMA
Downd: SMA -2*STD

This measure volatility but most importantly overbuying and overselling
More than 1 interpreation
and it should be used with outher tech indicators

Buying strategy:
In this example we are selling when the upper trend is crossed and we are buying when the down is crossed

Problem is you can have more buy signal than sell signal ( vice versa )
We handll the following way:

    we open in the first buying signal and ignore the other
    we close in the first selling signal and ignore the other

Ha elemezzuk akkor kiderul hogy ez nem teljesit jol bear marketben

backtesting: buys and sells into df
'''

from dataScraping.GetHistoricalData import GetHistoricalData
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from strategies.Strategy import Strategy


class BollingerBand(Strategy):

    df = pd.DataFrame()

    def __init__(self,ticker,interval):
        temp = GetHistoricalData(ticker,  interval)


    def retrieveData(self):
        pass

    def createDF(self):
        pass

    def plot(self):
        pass


temp = GetHistoricalData('BTCUSDT', '1d')
temp.getDataBetweenDates('2022-01-01', '2022-06-25')

df = temp.readData()
df = df.set_index('Time')
# calc sma, std upper and lower band and signal and clear na:

df['SMA'] = df.Close.rolling(window=20).mean()
df['STD'] = df.Close.rolling(window=20).std()
df['upper'] = df.SMA + 2 * df.STD
df['lower'] = df.SMA - 2 * df.STD
df['Buy_Signal'] = np.where(df.lower > df.Close, True, False)
df['Sell_Signal'] = np.where(df.upper < df.Close, True, False)
df = df.dropna()
print(df)

# plotting the results

plt.figure(figsize= (25,6))
plt.plot(df[['Close', 'SMA', 'upper', 'lower']])
# x axis the time of buy_signal y Axis is the price at the price time
plt.scatter(df.index[df.Buy_Signal], df[df.Buy_Signal].Close, marker = '^', color = 'g')
plt.scatter(df.index[df.Sell_Signal], df[df.Sell_Signal].Close, marker = '^', color = 'y')
plt.fill_between(df.index, df.upper, df.lower, color = 'grey', alpha = 0.3)
plt.legend(['Close', 'SMA', 'upper', 'lower'])
plt.show()
