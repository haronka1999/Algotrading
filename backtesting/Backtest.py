"""
--------------------  Revision History: ----------------------------------------
* 2022-10-22    -   Class Created and first version created
--------------------------------------------------------------------------------
Video: https://www.youtube.com/watch?v=yTupVd6D9m8&ab_channel=Algovibes
Description:
    A class where performance measures and backtesting libraries are implemented

    The input parameter should be a sub instnace of Strategy.py and
    selldates, buydates, sellprices buyprices  attributes should be filled


Version Number: 1.0 V
--------------------------------------------------------------------------------
    - implemented relative returns and cumulative returns
-----------------------------------------------------------------------------------
"""
import pandas as pd

from strategies.BollingerBand import BollingerBand
from strategies.MeanReversion import MeanReversion
from strategies.Strategy import Strategy


def getFormattedSeries(series):
    index_name = []
    for i in range(len(series)):
        # reformat index
        index_name.append("Return for Trade " + str(i) + ": ")
        # reformat value
        series.iloc[i] = str(round(series.iloc[i] * 100, 2)) + " %"

    series.index = index_name
    return series


class Backtest:
    # noinspection PyProtectedMember
    def __init__(self, strategy):
        self._sellprices = strategy.buyprices
        self._buyprices = strategy.sellprices
        self.relative_returns = pd.Series(
            [(self._sellprices - self._buyprices) / self._buyprices for self._sellprices, self._buyprices
             in zip(self._sellprices, self._buyprices)])

    def get_relative_returns(self):
        return getFormattedSeries(self.relative_returns.copy())

    def get_cumulative_returns(self):
        cum_return = (self.relative_returns + 1).prod() - 1
        return str(round(cum_return * 100, 2)) + " %"

