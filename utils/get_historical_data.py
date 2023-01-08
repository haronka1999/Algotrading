import time
from datetime import datetime, timedelta
from utils.constants import Constants
from binance.client import Client
import pandas as pd
import sys


def check_date_validity(date_text):
    try:
        datetime.strptime(date_text, Constants.DATE_FORMAT)
    except ValueError:
        raise ValueError("Incorrect data format, should be yyyy-mm-dd")


class GetHistoricalData:
    """
    A utility class for getting the historical values for cryptocurrencies
    The class is responsible for fetching crypto related data from Binance

    Constructor is setting:
        ticker: the symbol of the asset. ex: BTCUSDT
        interval: how often should we get the data. ex 5m, 15m 20m, 1h etc.
        lookback: can be minutes or hours: example lookBack = '15 hours' or lookBack = '30 min'

    It needs to implement two type of data fetching:
        1. between two dates
        2. and data from the current date to a lookback period
    """

    def __init__(self, ticker: str, interval: str, lookback_time: str, start_date: str, end_date: str, api_key="", api_secret=""):
        """
        :param ticker: the symbol-pair of the given value. Ex. "BTCUSDT"
        :param interval:  the timestep for each data candle
        :param lookback_time: the time in hours or minutes of the retreiving
        :param start_date: the first day of the timeframe (format ex. 2022-12-25)
        :param end_date: the last day of the timeframe (Note: choose or lookback_time or the start_date and end_date)
        :param api_key:  the public key, generated from binance (if not given, trading is not possible)
        :param api_secret:  the secret key generated from binance (if not given, trading is not possible)
        """
        self.frame = pd.DataFrame()
        while True:
            try:

                self.client = Client(api_key, api_secret)
                # if the ping returns an empty dictionary the connection is established
                # otherwise an exception will be raised
                if not self.client.ping():
                    break

            except Exception as e:
                print("Error connection to client ", e)
                print("Retry in 5 seconds ... ")
                time.sleep(5)
                pass


        self.ticker = ticker
        self.interval = interval
        self.lookback_time = lookback_time
        self.start_date = start_date
        self.end_date = end_date
        self.check_parameters()
        self.populate_dataframe_from_binance()

    def populate_dataframe_from_binance(self):
        if self.start_date != Constants.NO_START_DATE and self.end_date != Constants.NO_END_DATE and self.lookback_time == Constants.NO_LOOKBACK_TIME:
            check_date_validity(self.start_date)
            check_date_validity(self.end_date)
            self.getDataBetweenDates(self.start_date, self.end_date)
        elif self.lookback_time != Constants.NO_LOOKBACK_TIME and self.start_date == Constants.NO_START_DATE and self.end_date == Constants.NO_END_DATE:
            self.retrieve_current_data(self.lookback_time)
        else:
            print("something wrong with the parameters, please try again")
            sys.exit()

    def check_parameters(self):
        if self.start_date == Constants.NO_START_DATE and self.end_date == Constants.NO_END_DATE and self.lookback_time == Constants.NO_LOOKBACK_TIME:
            print("No parameters were given.\nPlease give a lookback period or two dates!")
            sys.exit()

    def getDataFrame(self):
        return self.frame

    def getDataBetweenDates(self, startDate, endDate):
        self.frame = pd.DataFrame(
            self.client.get_historical_klines(symbol=self.ticker, start_str=startDate, end_str=endDate,
                                              interval=self.interval))
        self.clean_dataframe()

    def retrieve_current_data(self, lookBackTime):
        self.frame = pd.DataFrame(
            self.client.get_historical_klines(self.ticker, self.interval, lookBackTime + ' ago UTC'))
        self.clean_dataframe()

    def clean_dataframe(self):
        self.frame = self.frame.iloc[:, :6]
        self.frame.columns = Constants.COLUMN_LIST
        self.frame = self.frame.set_index(Constants.COLUMN_LIST[0])
        self.frame.index = pd.to_datetime(self.frame.index, unit='ms')
        self.frame.index = self.frame.index + timedelta(hours=2)
        self.frame = self.frame.astype(float)
