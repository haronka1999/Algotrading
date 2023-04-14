from fastapi import FastAPI, Request
import strategies
from strategies.bollinger_band import BollingerBand
from utils.constants import Constants

app = FastAPI()

@app.get(f"/strategy/current/bollinger-band")
def get_bollinger_band_strategy(ticker_symbol: str, interval: str, lookback: str, request: Request):
    """
    :param request:
    :param lookback:
    :param interval:
    :param ticker_symbol:
    :return: a pandas df converted to json, based on the Request for the specific Strategy
    """

    api_key = request.headers.get('api_key')
    api_secret = request.headers.get('api_secret')
    my_json = strategies.bollinger_band.BollingerBand(ticker=ticker_symbol, interval=interval,
                                                      lookback_time=lookback, start_date=Constants.NO_START_DATE,
                                                      end_date=Constants.NO_END_DATE,
                                                      api_key=api_key,
                                                      api_secret=api_secret).df.to_json()
    return my_json


"""
Api call example:
curl -X GET "http://127.0.0.1:8000/strategy/between-dates/bollinger-band?ticker_symbol=sds&interval=5m&start_date=12&end_date=14" -H "api_secret: secret H "api_key: key"
"""
@app.get("/strategy/between-dates/bollinger-band")
def get_bollinger_band_strategy(ticker_symbol: str, interval: str, start_date: str, end_date: str, request: Request):
    """
    :param request:
    :param ticker_symbol:
    :param interval:
    :param start_date: the first day of the timeframe (format ex. 2022-12-25)
    :param end_date: the last day of the timeframe (format ex. 2022-12-25)
    :return:
    """
    api_key = request.headers.get('api_key')
    api_secret = request.headers.get('api_secret')
    my_json = strategies.bollinger_band.BollingerBand(ticker=ticker_symbol, interval=interval,
                                                      lookback_time=Constants.NO_LOOKBACK_TIME,
                                                      start_date=start_date, end_date=end_date, api_key=api_key,
                                                      api_secret=api_secret).df.to_json()
    return my_json
