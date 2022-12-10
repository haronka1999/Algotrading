"""
--------------------  Revision History: ----------------------------------------
* 2022-10-15    -   Class Created
* 2022-10-21    -   Class getting first Version (1.0 V)
* 2022-10-24    -   Optimizing speed: storing dataframes in csv file
* 2022-11-16    -   Corrected the constructor's parameter list
* 2022-12-07    -   Refactoring: generalize lookbackperiod (it can be minutes and hours)
--------------------------------------------------------------------------------
Description:

The class is responsible for fetching crypto related data

Constructor is setting:
    ticker: the symbol of the asset. ex: BTCUSDT
    interval: how often should we get the data. ex 5m, 15m 20m, 1h etc
    lookback: can be minutes or hours: example lookBack = '15 hours' or lookBack = '30 min'

It needs to implement two type of data fetching:
    1. between two dates
    2. and data from the current date to a lookback period
"""
import os.path
from datetime import datetime

from utils.constants import no_start_date, no_end_date, no_lookback_time,COLUMN_LIST
from binance.client import Client
import pandas as pd
import sys

PATH_TO_DATAFILES = os.path.join('..', 'utils', 'dataFiles')
DATE_FORMAT = '%Y-%m-%d'


def check_date_validity(date_text):
    try:
        datetime.strptime(date_text, DATE_FORMAT)
    except ValueError:
        raise ValueError("Incorrect data format, should be yyyy-mm-dd")

class GetHistoricalData:

    def __init__(self, ticker, interval, lookback_time, start_date, end_date, api_key="", api_secret=""):
        self.frame = pd.DataFrame()
        self.client = Client(api_key, api_secret)
        self.ticker = ticker
        self.interval = interval
        self.lookback_time = lookback_time
        self.start_date = start_date
        self.end_date = end_date
        self.check_parameters()
        self.populate_dataframe_from_binance()

    def populate_dataframe_from_binance(self):
        if self.start_date != no_start_date and self.end_date != no_end_date and self.lookback_time == no_lookback_time:
            check_date_validity(self.start_date)
            check_date_validity(self.end_date)
            self.getDataBetweenDates(self.start_date, self.end_date)
        elif self.lookback_time != no_lookback_time and self.start_date == no_start_date and self.end_date == no_end_date:
            self.retrieve_current_data(self.lookback_time)
        else:
            print("something wrong with the parameters, please try again")
            sys.exit()

    def check_parameters(self):
        if self.start_date == no_start_date and self.end_date == no_end_date and self.lookback_time == no_lookback_time:
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
        self.frame.columns = COLUMN_LIST
        self.frame.Time = self.frame.Time.astype(float)
        self.frame.Time = pd.to_datetime(self.frame.Time / 1000, unit='s')
        self.frame = self.frame.set_index(COLUMN_LIST[0])
        self.frame.Open = self.frame.Open.astype(float)
        self.frame.High = self.frame.High.astype(float)
        self.frame.Low = self.frame.Low.astype(float)
        self.frame.Close = self.frame.Close.astype(float)


# he = GetHistoricalData(ticker="ADAUSDT", startDate="2022-05-12", endDate=today, lookbackHours="-1",interval="1d")

