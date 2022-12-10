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
from utils.get_historical_data import GetHistoricalData
from utils import utilities


class Strategy:
    def __init__(self, ticker, interval, lookback_time, start_date, end_date, api_key="", api_secret=""):

        if api_key == "" and api_secret == "":
            data = GetHistoricalData(ticker, interval, lookback_time, start_date, end_date, api_key="", api_secret="")
        else:
            data = GetHistoricalData(ticker, interval, lookback_time, start_date, end_date, api_key=api_key, api_secret=api_secret)


        self.df = data.getDataFrame()

        self.buydates = []
        self.selldates = []
        self.buyprices = []
        self.sellprices = []

    def merge_fear_and_greed_with_df(self):
        fear_and_greed_index = utilities.get_fear_and_greed_DF()
        if fear_and_greed_index.index.name != self.df.index.name:
            print("Index names are not the same cannot join")
            sys.exit()
        return self.df.merge(fear_and_greed_index, on=fear_and_greed_index.index.name)

    @abstractmethod
    def calculate_values_for_df(self):
        pass

    @abstractmethod
    def plot(self):
        pass
