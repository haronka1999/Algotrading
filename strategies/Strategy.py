"""
--------------------  Revision History: ----------------------------------------
* 2022-10-15    -   Class Created
* 2022-10-21    -   Class getting first Version (1.0 V)
* 2022-10-22    -   The constructor is initialized here and moved here from sub classes
                and the selldates, buydates, sellprices buyprices attributes are moved from the sub classes
* 2022-10-24    -   Adding fearAndGreedIndex

--------------------------------------------------------------------------------
Version Number: 1.4 V
Description:

    Base class for every strategy which will be implemented
"""

import sys
from abc import abstractmethod

from utils.Utilities import today
from utils.dataScraping.GetHistoricalData import GetHistoricalData
from utils import Utilities


class Strategy:
    def __init__(self, ticker, interval, columns, lookbackHours='-1', startDate='noStartDate', endDate=today):
        if lookbackHours != '-1':
            data = GetHistoricalData(ticker, interval, lookbackHours=lookbackHours)
        elif startDate != 'noStartDate':
            data = GetHistoricalData(ticker, interval, startDate=startDate, endDate=endDate)
        else:
            print("something wrong with the parameters please try again")
            sys.exit()
        self.df = data.getDataFrame()
        # basic data cleaning
        column_len = len(columns)
        self.df = self.df.iloc[:, :column_len]
        self.df.columns = columns
        self.columns = columns
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
