"""
--------------------  Revision History: ----------------------------------------
* 2022-10-15    -   Class Created
* 2022-10-26    -   Added fear and greed
* 2022-11-16    -   Added getStrategyClassNames and  createStrategyInstanceFromString
--------------------------------------------------------------------------------
Description:

    General utility class for usage in the whole project
"""

import os
import re
from datetime import date, timedelta
import requests
import pandas as pd

# format: yyyy-mm-dd
today = date.today().strftime("%Y-%m-%d")
yesterday = date.today() - timedelta(days=1)

"""
Possible strategies with fear and greed:
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


# this is used for generating class names so the User can see in the UI
def getStrategyClassNames():
    classNames = []
    directory = 'C:\\AlgoTrading\\strategies'
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            with open(os.path.join(directory, filename)) as topo_file:
                # retrieve the className of the file:
                classNames.append(re.search("class (.*)(Strategy)", topo_file.read()).group(1)[:-1])

    while "" in classNames:
        classNames.remove("")

    return classNames
