"""
--------------------  Revision History: ----------------------------------------
* 2022-10-15    -   Class Created
* 2022-10-21    -   Class getting first Version (1.0 V)
--------------------------------------------------------------------------------
Version Number: 1.0 V

Description:

The class is responsible for fetching crypto related data

Constructor is setting:
    ticker: the symbol of the asset. ex: BTCUSDT
    interval: how often should we get the data. ex 5m, 15m 20m, 1h etc

It needs to implement two type of data fetching:
    1. between two dates
    2. and data from the current date to a lookback period
"""

from datetime import datetime
from utils.secret.SecretKeys import api_key, api_secret
from binance.client import Client
import pandas as pd
import sys


DATE_FORMAT = '%Y-%m-%d'
COLUMN_LIST = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume',
               'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']


def validate(date_text):
    try:
        datetime.strptime(date_text, DATE_FORMAT)
    except ValueError:
        raise ValueError("Incorrect data format, should be yyyy-mm-dd")


class GetHistoricalData:
    frame = pd.DataFrame()
    client = Client(api_key, api_secret)

    def __init__(self, ticker, interval, lookbackHours='-1', startDate='noStartDate', endDate='noEndDate'):
        self.ticker = ticker
        self.interval = interval
        self.fileName = ticker + '-' + interval
        if startDate == 'noStartDate' and endDate == 'noEndDate' and lookbackHours == '-1':
            print("No parameters were given.\nPlease give a lookback period or two dates!")
            sys.exit()

        if startDate != 'noStartDate' and endDate != 'noEndDate' and lookbackHours == '-1':
            validate(startDate)
            validate(endDate)
            self.getDataBetweenDates(startDate, endDate)
        elif lookbackHours != '-1':
            self.getCurrentData(lookbackHours)
        else:
            print("something wrong with the parameters, please try again")
            sys.exit()

    def getDataFrame(self):
        return self.frame

    def cleanDataFrame(self):
        self.frame.columns = COLUMN_LIST
        self.frame.Time = pd.to_datetime(self.frame.Time, unit='ms')
        self.frame.Time = self.frame.Time + pd.Timedelta(hours=3)
        self.frame.Open = self.frame.Open.astype(float)
        self.frame.High = self.frame.High.astype(float)
        self.frame.Low = self.frame.Low.astype(float)
        self.frame.Close = self.frame.Close.astype(float)

    def getDataBetweenDates(self, startDate, endDate):
        self.frame = pd.DataFrame(
            self.client.get_historical_klines(symbol=self.ticker, start_str=startDate, end_str=endDate,
                                              interval=self.interval))
        self.cleanDataFrame()

    def getCurrentData(self, lookBackHours):
        self.frame = pd.DataFrame(
            self.client.get_historical_klines(self.ticker, self.interval, lookBackHours + ' hours ago UTC'))
        self.cleanDataFrame()

    def createPickle(self, lookBackHours='1', startDate='noStartDate', endDate='noEndDate'):

        if lookBackHours != '-1':
            self.fileName = self.fileName + '-' + lookBackHours + 'h' + '.pkl'
        elif startDate != 'noStartDate' and endDate != 'noEndDate':
            self.fileName = self.fileName + '-' + startDate + '-' + endDate + '.pkl'

        self.frame.to_pickle(self.fileName)
        print(self.fileName + "successfully created ! ")

    def readData(self):
        return pd.read_pickle(self.fileName)



# testing:
# data = GetHistoricalData('BTCUSDT', '1h', lookbackHours='75')
# df = data.getDataFrame()
# print(df)
