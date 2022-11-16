"""
--------------------  Revision History: ----------------------------------------
# 2022-11-11    -   Class created basic functionalities implemented
* 2022-11-16    -   Deleted default values for constructor's parameter list (it is handled in the UI side)
--------------------------------------------------------------------------------
Video: -
Description
TODO: add description, search video and understand logic

---------------------------------------------------------------------------
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from strategies.Strategy import Strategy


class RollMaxRollMin(Strategy):
    df = pd.DataFrame()
    COLUMN_LIST = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']

    def __init__(self, ticker, interval, columns, lookbackHours, startDate, endDate):
        super(RollMaxRollMin, self).__init__(ticker, interval, columns, lookbackHours, startDate, endDate)
        # clean the dataframe and set values for column
        self._calculateValuesForDf(columns)
        print(self.df)

    def _calculateValuesForDf(self, columns):
        self.df['rollHigh'] = self.df.High.rolling(15).max()
        self.df['rollLow'] = self.df.Low.rolling(15).min()
        self.df['mid'] = (self.df['rollHigh'] + self.df['rollLow']) / 2

        # selling: this is 1 if the close is near to rolling maximum
        self.df['highapproach'] = np.where(self.df.Close > self.df.rollHigh * 0.996, 1, 0)

        # buying: close is aboce the midline
        self.df['close_a_mid'] = np.where(self.df.Close > self.df.mid, 1, 0)
        # if midcross is true and we are in a position
        self.df['midcross'] = self.df.close_a_mid.diff() == 1

    def plot(self):
        buydates, selldates = self._getPositions()
        plt.figure(figsize=(22, 16))
        plt.plot(self.df[['Close', 'rollHigh', 'rollLow', 'mid']])
        plt.scatter(buydates, self.df.loc[buydates].Open, marker='^', color='g', s=200)
        plt.scatter(selldates, self.df.loc[selldates].Open, marker='v', color='b', s=200)
        plt.show()

    def _getPositions(self):
        in_position = False
        buydates, selldates = [], []

        for i in range(len(self.df) - 23):
            if not in_position:
                # check buying cond:
                if self.df.iloc[i].midcross:
                    # setting up a stop loss: 5%
                    if (self.df.iloc[i + 5].Close / self.df.iloc[i].Close) > 0.05:
                        # we only can buy in the next timestep
                        buydates.append(self.df.iloc[i + 1].name)
                        in_position = True

            if in_position:
                if self.df.iloc[i].highapproach:
                    # we only can buy in the next timestep
                    selldates.append(self.df.iloc[i + 1].name)
                    in_position = False

        return buydates, selldates

