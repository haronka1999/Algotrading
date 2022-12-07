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

from utils.constants import noStartDate, noEndDate, noLookBackHours,COLUMN_LIST
from binance.client import Client
import pandas as pd
import sys

PATH_TO_DATAFILES = os.path.join('..', 'utils', 'dataFiles')
DATE_FORMAT = '%Y-%m-%d'


def checkDateValidity(date_text):
    try:
        datetime.strptime(date_text, DATE_FORMAT)
    except ValueError:
        raise ValueError("Incorrect data format, should be yyyy-mm-dd")

class GetHistoricalData:

    def __init__(self, ticker, interval, lookBackTime, startDate, endDate, api_key="", api_secret=""):
        self.frame = pd.DataFrame()
        self.client = Client(api_key, api_secret)
        self.ticker = ticker
        self.interval = interval
        self.lookBackTime = lookBackTime
        self.startDate = startDate
        self.endDate = endDate
        self._checkParameters()
        self._populateDataFrameFromBinance()

    def _populateDataFrameFromBinance(self):
        if self.startDate != noStartDate and self.endDate != noEndDate and self.lookBackTime == noLookBackHours:
            checkDateValidity(self.startDate)
            checkDateValidity(self.endDate)
            self.getDataBetweenDates(self.startDate, self.endDate)
        elif self.lookBackTime != noLookBackHours and self.startDate == noStartDate and self.endDate == noEndDate:
            self.getCurrentData(self.lookBackTime)
        else:
            print("something wrong with the parameters, please try again")
            sys.exit()

    def _checkParameters(self):
        if self.startDate == noStartDate and self.endDate == noEndDate and self.lookBackTime == noLookBackHours:
            print("No parameters were given.\nPlease give a lookback period or two dates!")
            sys.exit()

    def getDataFrame(self):
        return self.frame

    def getDataBetweenDates(self, startDate, endDate):
        self.frame = pd.DataFrame(
            self.client.get_historical_klines(symbol=self.ticker, start_str=startDate, end_str=endDate,
                                              interval=self.interval))
        self._cleanDataFrame()

    def getCurrentData(self, lookBackTime):
        self.frame = pd.DataFrame(
            self.client.get_historical_klines(self.ticker, self.interval, lookBackTime + ' ago UTC'))
        self._cleanDataFrame()

    def _cleanDataFrame(self):
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

