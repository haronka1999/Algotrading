'''


'''

import pandas as pd
from binance.client import Client

class GetHistoricalData:
    api_key = 'RowNIh7ob9TxTu3V9xLKtDY9JD3x2e8k8xPGLtDfEd7ORxX3ZH9FNW4DbBcSAcTL'
    api_secret = 'CaWH0MyeinSIAdqeE3XCVuF0SMqxEDcM40YS7COSt8w9sgy0RoZnfa4TZjhptVbG'
    frame = pd.DataFrame()
    client = Client(api_key, api_secret)

    def __init__(self, ticker, interval):
        self.ticker = ticker
        self.interval = interval
        self.fileName = ticker + '-' + interval

    def cleanDataFrame(self):
        self.frame = self.frame.iloc[:, :6]
        self.frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        self.frame.Time = pd.to_datetime(self.frame.Time, unit='ms')
        self.frame.Time = self.frame.Time + pd.Timedelta(hours=3)
        self.frame.Open = self.frame.Open.astype(float)
        self.frame.High = self.frame.High.astype(float)
        self.frame.Low = self.frame.Low.astype(float)
        self.frame.Close = self.frame.Close.astype(float)

    def getDataBetweenDates(self, startdate, enddate):
        self.frame = pd.DataFrame(
            self.client.get_historical_klines(symbol=self.ticker, start_str=startdate, end_str=enddate,
                                              interval=self.interval))
        self.cleanDataFrame()
        self.fileName = self.fileName + '-' + startdate + '-' + enddate + '.pkl'
        self.frame.to_pickle(self.fileName)
        print(self.fileName + "successfully created ! ")

    def getCurrentData(self, lookback):
        self.frame = pd.DataFrame(
            self.client.get_historical_klines(self.ticker, self.interval, lookback + ' hours ago UTC'))
        self.cleanDataFrame()
        self.fileName = self.fileName + '-' + lookback + 'h' + '.pkl'
        self.frame.to_pickle(self.fileName)
        print(self.fileName + "successfully created ! ")

    def printDf(self):
        print(self.frame)

    def readData(self):
        try:
            return pd.read_pickle(self.fileName)
        except:
            print("No file created yet! ")
            return

# data = GetHistoricalData('BTCUSDT', '1h')
# data.getDataBetweenDates('75')


