import requests
import pandas as pd

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
