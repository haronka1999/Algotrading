"""
--------------------  Revision History: ----------------------------------------
* 2022-10-15    -   Class Created
* 2022-10-21    -   Class getting first Version (1.0 V)
* 2022-10-22    -   The constructor is initialized here and moved here from sub classes
                and the selldates, buydates, sellprices buyprices attributes are moved from the sub classes
* 2022-10-24    -   Adding fearAndGreedIndex
* 2022-11-16    -   Deleted default values for constructor's parameter list (it is handled in the UI side)
* 2022-11-24    -   Code reformatting: moved checking into GetHistoricalData and  implement the two separate
                    data retrieval method
--------------------------------------------------------------------------------
Description:

    Base class for every strategy which will be implemented
"""

import sys
from abc import abstractmethod
from utils.GetHistoricalData import GetHistoricalData, RetrieveDataFromYFinance
from utils import Utilities


class Strategy:
    def __init__(self, ticker, interval, columns, lookbackHours, startDate, endDate, isBinance=False):

        if isBinance:
            data = GetHistoricalData(ticker, interval, lookbackHours, startDate, endDate)
        else:
            data = RetrieveDataFromYFinance()

        self.df = data.getDataFrame()

        self.buydates = []
        self.selldates = []
        self.buyprices = []
        self.sellprices = []

    def mergeFearAndGreedWithDf(self):
        fearAndGreedIndex = Utilities.getFearAndGreedDf()
        if fearAndGreedIndex.index.name != self.df.index.name:
            print("Index names are not the same cannot join")
            sys.exit()
        return self.df.merge(fearAndGreedIndex, on=fearAndGreedIndex.index.name)

    @abstractmethod
    def _calculateValuesForDf(self, columns):
        pass

    @abstractmethod
    def plot(self):
        pass
