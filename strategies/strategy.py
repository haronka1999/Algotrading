import sys
from abc import abstractmethod
import utils
from utils import get_historical_data
# from utils import utility_methods


class Strategy:
    """
    Base class for every strategy which will be implemented
    """
    def __init__(self, ticker, interval, lookback_time, start_date, end_date, api_key="", api_secret=""):

        self.ticker = ticker
        self.interval = interval
        self.lookback_time = lookback_time
        self.start_date = start_date
        self.end_date = end_date
        self.api_key = api_key
        self.api_secret = api_secret

        if api_key == "" and api_secret == "":
            data = get_historical_data.GetHistoricalData(ticker, interval, lookback_time, start_date, end_date, api_key="", api_secret="")
        else:
            data = get_historical_data.GetHistoricalData(ticker, interval, lookback_time, start_date, end_date, api_key=api_key, api_secret=api_secret)

        self.df = data.getDataFrame()

        self.buydates = []
        self.selldates = []
        self.buyprices = []
        self.sellprices = []

    # def merge_fear_and_greed_with_df(self):
    #     fear_and_greed_index = utility_methods.get_fear_and_greed_DF()
    #     if fear_and_greed_index.index.name != self.df.index.name:
    #         print("Index names are not the same cannot join")
    #         sys.exit()
    #     return self.df.merge(fear_and_greed_index, on=fear_and_greed_index.index.name)

    @abstractmethod
    def calculate_values_for_df(self):
        pass

    @abstractmethod
    def plot(self):
        pass
