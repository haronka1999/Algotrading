"""
--------------------  Revision History: ----------------------------------------
# 2022-11-24    -   Class created
--------------------------------------------------------------------------------
Description:
    Implementing helper functions for UI
---------------------------------------------------------------------------
"""

from strategies import BollingerBand, MeanReversion, RegressionModels, StochRSIMACD


def createStrategyInstanceFromString(p_strategy, ticker_symbol, interval, column_list, lookBackHours, startDate, endDate):
    if p_strategy == "BollingerBand":
        return BollingerBand.BollingerBand(ticker_symbol, interval, column_list, lookBackHours, startDate,
                                           endDate)
    elif p_strategy == "MeanReversion":
        return MeanReversion.MeanReversion(ticker_symbol, interval, column_list, lookBackHours, startDate,
                                           endDate)
    elif p_strategy == "RegressionModels":
        return RegressionModels.RegressionModels(ticker_symbol, interval, column_list, lookBackHours,
                                                 startDate, endDate)
    elif p_strategy == "StochRSIMACD":
        return StochRSIMACD.StochRSIMACD(ticker_symbol, interval, column_list, lookBackHours, startDate,
                                         endDate)
    else:
        return None


