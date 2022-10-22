import sys
from abc import abstractmethod

from dataScraping.GetHistoricalData import GetHistoricalData, validate


class Strategy:

    def __init__(self, ticker, interval, columns, lookbackHours='-1', startDate='noStartDate', endDate='noEndDate'):
        self.ticker = ticker
        self.interval = interval

        if lookbackHours != -1:
            data = GetHistoricalData(ticker, interval, lookbackHours=lookbackHours)
        elif startDate != 'noStartDate' and endDate != 'noEndDate':
            validate(startDate)
            validate(endDate)
            data = GetHistoricalData(ticker, interval, startDate=startDate, endDate=endDate)
        else:
            print("something wrong with the parameters please try again")
            sys.exit()
        self.df = data.getDataFrame()
        # clean the dataframe adn set values for column
        self.calculateValuesForDf(columns)

    @abstractmethod
    def calculateValuesForDf(self, columns):
        pass

    @abstractmethod
    def plot(self):
        pass


