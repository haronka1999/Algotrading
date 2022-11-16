"""
--------------------  Revision History: ----------------------------------------
* 2022-10-15    -   Class Created
* 2022-10-21    -   Class getting first Version (1.0 V)
* 2022-10-24    -   Optimizing speed: storing dataframes in csv file
* 2022-11-16    -   Corrected the constructor's parameter list
--------------------------------------------------------------------------------
Description:

The class is responsible for fetching crypto related data

Constructor is setting:
    ticker: the symbol of the asset. ex: BTCUSDT
    interval: how often should we get the data. ex 5m, 15m 20m, 1h etc

It needs to implement two type of data fetching:
    1. between two dates
    2. and data from the current date to a lookback period
"""
import os.path
from datetime import datetime

from utils.constants import noStartDate, noEndDate, noLookBackHours
from utils.secret.SecretKeys import api_key, api_secret
from binance.client import Client
import pandas as pd
import sys

FULL_COLUMN_LIST = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume',
                    'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']
PATH_TO_DATAFILES = os.path.join('..','utils', 'dataFiles')
DATE_FORMAT = '%Y-%m-%d'


def checkDateValidity(date_text):
    try:
        datetime.strptime(date_text, DATE_FORMAT)
    except ValueError:
        raise ValueError("Incorrect data format, should be yyyy-mm-dd")


class GetHistoricalData:
    frame = pd.DataFrame()
    client = Client(api_key, api_secret)

    def __init__(self, ticker, interval, lookbackHours, startDate, endDate):
        self.ticker = ticker
        self.interval = interval
        self.lookbackHours = lookbackHours
        self.startDate = startDate
        self.endDate = endDate
        self.fileName = self.getCSVFileName()
        self._checkParameters()
        isCSVFileExist = os.path.exists(os.path.join(PATH_TO_DATAFILES, self.fileName))

        # if the file already exist we can call them from there for speed optimizing purposes
        if not isCSVFileExist:
            self._populateDataFrameFromBinance()
        else:
            self.frame = self._loadCSVFileToDataFrame()

    def _populateDataFrameFromBinance(self):
        if self.startDate != noStartDate and self.endDate != noEndDate and self.lookbackHours == noLookBackHours:
            checkDateValidity(self.startDate)
            checkDateValidity(self.endDate)
            self.getDataBetweenDates(self.startDate, self.endDate)
        elif self.lookbackHours != noLookBackHours and self.startDate == noStartDate and self.endDate == noEndDate:
            self.getCurrentData(self.lookbackHours)
        else:
            print("something wrong with the parameters, please try again")
            sys.exit()

        # create a file so next time the data will be read from here
        self._createCSVFileFromDataFrame()

    def _checkParameters(self):
        if self.startDate == noStartDate and self.endDate == noEndDate and self.lookbackHours == noLookBackHours:
            print("No parameters were given.\nPlease give a lookback period or two dates!")
            sys.exit()

    def getCSVFileName(self):
        if self.lookbackHours != noLookBackHours:
            return self.ticker + '-' + self.interval + '-' + self.lookbackHours + 'h' + '.csv'
        elif self.startDate != noStartDate and self.endDate == noEndDate:
            return self.ticker + '-' + self.interval + '-' + self.startDate + '_' + self.endDate + '.csv'

    def getDataFrame(self):
        return self.frame

    def _cleanDataFrame(self):
        self.frame.columns = FULL_COLUMN_LIST
        print(type(self.frame.Time))
        self.frame.Time = pd.to_datetime(self.frame.Time / 1000, unit='s')
        self.frame.Open = self.frame.Open.astype(float)
        self.frame.High = self.frame.High.astype(float)
        self.frame.Low = self.frame.Low.astype(float)
        self.frame.Close = self.frame.Close.astype(float)

    def getDataBetweenDates(self, startDate, endDate):
        self.frame = pd.DataFrame(
            self.client.get_historical_klines(symbol=self.ticker, start_str=startDate, end_str=endDate,
                                              interval=self.interval))

        self._cleanDataFrame()

    def getCurrentData(self, lookBackHours):
        self.frame = pd.DataFrame(
            self.client.get_historical_klines(self.ticker, self.interval, lookBackHours + ' hours ago UTC'))
        self._cleanDataFrame()

    def _createCSVFileFromDataFrame(self):
        if self.fileName != '':
            fullPathToFile = os.path.join(PATH_TO_DATAFILES, self.fileName)
            self.frame.to_csv(fullPathToFile, index=False)
        else:
            print(" THe name for the data file is not populated")
            sys.exit()

    def _loadCSVFileToDataFrame(self):
        return pd.read_csv(os.path.join(PATH_TO_DATAFILES, self.fileName))

# testing:
# data = GetHistoricalData('BTCUSDT', '1h', lookbackHours='75')
# df = data.getDataFrame()
# print(df)
