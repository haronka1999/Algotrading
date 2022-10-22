"""
--------------------  Revision History: ----------------------------------------
* 2022-10-22    -   Class Created
--------------------------------------------------------------------------------
Version Number: 1.0 V

Description
Video: https://www.youtube.com/watch?v=AXc1YAsCduI&ab_channel=Algovibes
Article: https://www.linkedin.com/pulse/algorithmic-trading-mean-reversion-using-python-bryan-chen/

Strategy: if a stock is going up than we can sell and if it goes down it we can buy

Notes:
    - it is good in sideways market
    - we can create stop loss but it will cannot skop black - swan events and it will
    decrease performance
-----------------------------------------------------------------------------------
"""

import sys

from dataScraping.GetHistoricalData import GetHistoricalData, validate, BOLLINGER_COLUMN_LIST
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from strategies.Strategy import Strategy

class MeanReversion(Strategy):
    ticker = ""
    interval = ""
    df = pd.DataFrame()

    def __init__(self, ticker, interval, columns, lookbackHours='-1', startDate='noStartDate', endDate='noEndDate'):
        super(MeanReversion, self).__init__(ticker, interval, columns, lookbackHours, startDate, endDate)
        pass

    # calculate sma, std upper and lower band and signal and clear na:
    def calculateValuesForDf(self, columns):
        pass


    def plot(self):
        pass

    def backTest(self):
        pass

    # test the class


meanReversion = MeanReversion('BTCUSDT', '30m', BOLLINGER_COLUMN_LIST, lookbackHours='130  ')

