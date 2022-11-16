"""
--------------------  Revision History: ----------------------------------------
# 2022-10-24    -   Class created and stuck with no buying signals
* 2022-11-16    -   Deleted default values for constructor's parameter list (it is handled in the UI side)
--------------------------------------------------------------------------------
Video: https://www.youtube.com/watch?v=4MnNft7Squk
Description

Check if the previous four data candle and the following 4 candle
data's High value is smaller than the actual data's High vale
-----------------------------------------------------------------------------------
"""
import numpy as np
import pandas as pd
import ta.trend
from strategies.Strategy import Strategy


class WilliamFractal(Strategy):
    df = pd.DataFrame()
    COLUMN_LIST = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    CANDLE_LOOKBACK = 4

    def __init__(self, ticker, interval, columns, lookbackHours, startDate, endDate):
        super(WilliamFractal, self).__init__(ticker, interval, columns, lookbackHours, startDate, endDate)
        # clean the dataframe and set values for column
        self._calculateValuesForDf(columns)
        print(self.df.head(30))

    # TODO: somehow doesn't fill with buy values ?? (video 9 minutes somewhere)
    def _calculateValuesForDf(self, columns):
        self.df = self.df.set_index('Time')
        self.df['EMA_200'] = ta.trend.ema_indicator(self.df.Close, window=200)
        # calculate fractals: 4 + 1 + 4: True where the theory is fulfilled (local maxima)
        self.df['wf_top_bool'] = np.where(
            self.df['High'] == self.df['High'].rolling(2 * self.CANDLE_LOOKBACK + 1, center=True).max(), True, False)

        self.df['wf_top'] = np.where(
            self.df['High'] == self.df['High'].rolling(2 * self.CANDLE_LOOKBACK + 1, center=True).max(),
            self.df['High'], None)
        self.getConsecutiveValues()
        self.df = self.df.dropna()
        self.df['buy'] = np.where((self.df.Close > self.df.wf_top) & (self.df.Close > self.df.EMA_200), 1, 0)
        self.df.to_csv("file.csv")

    def plot(self):
        pass

    def getConsecutiveValues(self):
        temp_series_top = self.df['wf_top'].copy()
        ind = 0
        while ind < len(temp_series_top) - self.CANDLE_LOOKBACK:
            if temp_series_top[ind] is not None and temp_series_top[ind] > 0:
                for fill_ind in range(1, self.CANDLE_LOOKBACK + 1):
                    temp_series_top.iloc[ind + fill_ind] = temp_series_top[ind]
                ind = ind + 4
            ind += 1

        self.df['wf_top'] = temp_series_top
        self.df['wf_top'] = self.df['wf_top'].replace(0, np.NaN)