"""
--------------------  Revision History: ----------------------------------------
# 2022-11-24    -   Class created
--------------------------------------------------------------------------------
Description:
    Implementing helper functions for UI
---------------------------------------------------------------------------
"""

from strategies import BollingerBand, MeanReversion, RegressionModels, StochRSIMACD
import re



def createStrategyInstanceFromString(p_strategy, ticker_symbol, interval, lookBackHours, startDate,
                                     endDate, api_key="", api_secret=""):
    if p_strategy == "BollingerBand":
        return BollingerBand.BollingerBand(ticker_symbol, interval, lookBackHours, startDate,
                                           endDate, api_key, api_secret)
    elif p_strategy == "MeanReversion":
        return MeanReversion.MeanReversion(ticker_symbol, interval, lookBackHours, startDate,
                                           endDate,api_key, api_secret)
    elif p_strategy == "RegressionModels":
        return RegressionModels.RegressionModels(ticker_symbol, interval, lookBackHours,
                                                 startDate, endDate,api_key, api_secret)
    elif p_strategy == "StochRSIMACD":
        return StochRSIMACD.StochRSIMACD(ticker_symbol, interval, lookBackHours, startDate,
                                         endDate,api_key, api_secret)
    else:
        return None


def validateInputs(ticker_symbol, interval, lookBackHours, startDate, endDate):
    if ticker_symbol == "":
        return "Ticker  field is empty"
    if any(not c.isalnum() for c in ticker_symbol) and ticker_symbol.isnumeric():
        return "Ticker symbol contains unallowed characters"

    if interval == "":
        return "Interval  field is empty"

    if not re.match('^(\d*\d){1,2}[h,d,m]$', interval):
        return "The Interval is not in correct format"
    return ""
