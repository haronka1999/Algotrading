"""
--------------------  Revision History: ----------------------------------------
# 2022-11-24    -   Class created
--------------------------------------------------------------------------------
Description:
    Implementing helper functions for UI
---------------------------------------------------------------------------
"""

from strategies import bollinger_band, mean_reversion, regression_models, stoch_RSI_MACD
import re


def create_strategy_instance_from_string(p_strategy, ticker_symbol, interval, lookback_time, start_date,
                                         end_date, api_key="", api_secret=""):
    if p_strategy == "BollingerBand":
        return bollinger_band.BollingerBand(ticker_symbol, interval, lookback_time, start_date,
                                            end_date, api_key, api_secret)
    elif p_strategy == "MeanReversion":
        return mean_reversion.MeanReversion(ticker_symbol, interval, lookback_time, start_date,
                                            end_date, api_key, api_secret)
    elif p_strategy == "RegressionModels":
        return regression_models.RegressionModels(ticker_symbol, interval, lookback_time,
                                                  start_date, end_date, api_key, api_secret)
    elif p_strategy == "StochRSIMACD":
        return stoch_RSI_MACD.StochRSIMACD(ticker_symbol, interval, lookback_time, start_date,
                                           end_date, api_key, api_secret)
    else:
        return None


def validateInputs(ticker_symbol, interval):
    if ticker_symbol == "":
        return "Ticker  field is empty"
    if any(not c.isalnum() for c in ticker_symbol) and ticker_symbol.isnumeric():
        return "Ticker symbol contains unallowed characters"

    if interval == "":
        return "Interval  field is empty"

    if not re.match('^(\d*\d){1,2}[h,d,m]$', interval):
        return "The Interval is not in correct format"
    return ""
