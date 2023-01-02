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
import os
import streamlit as st
from feedparser import parse
from bs4 import BeautifulSoup
from utils.constants import Constants
from utils.get_historical_data import GetHistoricalData
import requests
import pandas as pd

def get_fear_and_greed_DF() -> pd.DataFrame:
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

def get_strategy_class_names() -> list[str]:
    """
    use for generating class names so the User can see in the UI
    :return:  a list with the strategy classnames
    """
    class_names = []
    directory = os.path.join("..", "..", "AlgoTrading", "strategies")
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            with open(os.path.join(directory, filename)) as topo_file:
                # retrieve the className of the file:
                class_names.append(re.search("class (.*)(Strategy)", topo_file.read()).group(1)[:-1])

    while "" in class_names:
        class_names.remove("")
    return class_names



def get_crypto_prices(ticker_list: list) -> pd.DataFrame:
    """
    Generate a dataframe with the latest crypt prices
    :param ticker_list:  the  cryptocurrencies which will be included
    :return: The dataframe with the values of the latest Close values. Will refresh after page refresh
    """
    price_col_values = []
    last_time_updated = []
    for symbol in ticker_list:
        crypto_price = GetHistoricalData(symbol, "1m", "3 min", Constants.NO_START_DATE, Constants.NO_END_DATE)
        # convert to datetime so we can extract only the time than cut the seconds from the end of the string
        last_time_updated.append(str(pd.to_datetime(crypto_price.frame.iloc[-1].name).time())[:-3])
        price_col_values.append(crypto_price.frame.Close.iloc[-1])
    df = pd.DataFrame({"Symbol": ticker_list, "Price": price_col_values, "Last Updated": last_time_updated})
    return df


def add_articles(articles):
    no_of_articles = len(articles)
    article_index = 0
    col_index = -1
    while True:
        article = articles[article_index]
        title = article["title"]
        link = article["link"]
        date = article["pub_date"]
        st.markdown(f"### [{title}]({link})")
        if article["image"] is None:
            if "nulltx" in link:
                st.image("https://nulltx.com/wp-content/uploads/2018/10/nulltx-logo-red.png")
            if "cryptoslate" in link:
                st.image("https://cryptoslate.com/wp-content/themes/cryptoslate-2020/images/cs-media-logo-dark.png",
                         width=320)
        else:
            st.image(article["image"])
        st.caption(f"{date}")
        st.write(article["summary"])

        if no_of_articles == article_index + 1:
            return

        article_index += 1
        col_index *= -1


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


def generate_articles():
    item_attr_map = {
        "https://cointelegraph.com/rss": {"title": "title",
                                          "link": "link", "pub_date": "published",
                                          "summary": {"summary": ("p", 1, "text")},
                                          "image": {"summary": ("img", "src")}},
    }

    rss_articles = []
    for url in item_attr_map.keys():
        feed = parse(url)
        items = feed['entries']
        for item in items:
            attrs = item_attr_map[url]
            article = {}
            for key, val in attrs.items():
                if key == "pub_date":
                    article[key] = item[val][5:-5]
                elif type(val) == str:
                    article[key] = item[val]
                elif val is None:
                    article[key] = None

                elif type(val) == dict:
                    nested_key = list(val.keys())[0]
                    nested_val = val[nested_key]
                    soup = BeautifulSoup(item[nested_key], features="lxml")
                    if val[nested_key] == "text":
                        article[key] = soup.text
                    elif type(nested_val) == tuple:
                        if nested_key == "summary":
                            if len(nested_val) == 2:
                                article["summary"] = soup.text
                            elif len(nested_val) == 3:
                                article["summary"] = soup.find_all(
                                    [nested_val[0]])[nested_val[1]].text
                        if key == "image":
                            article["image"] = soup.find([nested_val[0]]).get(nested_val[1])
            rss_articles.append(article)
    return rss_articles
