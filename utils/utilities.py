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


class Utilities:
    # format: yyyy-mm-dd
    today = date.today().strftime("%Y-%m-%d")
    yesterday = date.today() - timedelta(days=1)

    def get_fear_and_greed_DF(self) -> pd.DataFrame:
        """
        Possible strategies with fear and greed:
            - Hold an asset until the fear and greed index is above 5
            Notes:
             - This should be used with an existing strategy
        :return the dataframe with the fear and greed index. Possible merge by the dates
        """
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

