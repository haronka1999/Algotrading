"""
--------------------  Revision History: ----------------------------------------
* 2022-10-15    -   Class Created
* 2022-10-26    -   Added fear and greed
* 2022-11-16    -   Added getStrategyClassNames and  createStrategyInstanceFromString
--------------------------------------------------------------------------------
Description:

    The use should be able to choose an existing strategy and backtest it in multiple timeframes
"""

import os
import re
from datetime import date, datetime, timedelta
import requests
import pandas as pd
from strategies import BollingerBand, MeanReversion, RegressionModels, RollMaxRollMin, StochRSIMACD, WilliamFractal

# format: yyyy-mm-dd

today = date.today().strftime("%Y-%m-%d")
yesterday = date.today() - timedelta(days=1)


"""
Possible strategies:
    - Hold an asset until the fear and greed index is above 50
    
    Notes:
     - This should be used with an existing strategy 
"""
def getFearAndGreedDf():
    url = "https://api.alternative.me/fng/?limit=0"
    r = requests.get(url)
    df = pd.DataFrame(r.json()['data'])
    df.value = df.value.astype(int)
    df.timestamp = pd.to_datetime(df.timestamp, unit='s')
    df = df.set_index('timestamp')
    df.index.name = 'Date'
    # revert to be the first date last
    df = df[::-1]
    return df





# create an instance for every strategy based on the chosen string
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
    elif p_strategy == "RollMaxRollMin":
        return RollMaxRollMin.RollMaxRollMin(ticker_symbol, interval, column_list, lookBackHours, startDate,
                                             endDate)
    elif p_strategy == "StochRSIMACD":
        return StochRSIMACD.StochRSIMACD(ticker_symbol, interval, column_list, lookBackHours, startDate,
                                         endDate)
    elif p_strategy == "WilliamFractal":
        return WilliamFractal.WilliamFractal(ticker_symbol, interval, column_list, lookBackHours, startDate,
                                             endDate)
    else:
        return None


# this is used for generating class names so the User can see in the UI
def getStrategyClassNames():
    classNames = []
    directory = "strategies"
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            with open(os.path.join(directory, filename)) as topo_file:
                # retrieve the className of the file:
                classNames.append(re.search("class (.*)(Strategy)", topo_file.read()).group(1)[:-1])

    while "" in classNames:
        classNames.remove("")

    return classNames


