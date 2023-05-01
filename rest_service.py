from fastapi import FastAPI, Request
import strategies
from strategies.bollinger_band import BollingerBand
from strategies.mean_reversion import MeanReversion
from strategies.stoch_RSI_MACD import StochRSIMACD
from utils.constants import Constants

app = FastAPI()

"""
Run rest service with the following command:
uvicorn rest_service:app --host 0.0.0.0 --port 8000
"""


@app.get("/strategy/bollinger-band/lookback/{ticker_symbol}/{interval}/{lookback}")
def get_bollinger_band_strategy(ticker_symbol: str, interval: str, lookback: str, request: Request):
    api_key = request.headers.get('api_key')
    api_secret = request.headers.get('api_secret')
    my_json = strategies.bollinger_band.BollingerBand(ticker=ticker_symbol, interval=interval,
                                                      lookback_time=lookback, start_date=Constants.NO_START_DATE,
                                                      end_date=Constants.NO_END_DATE,
                                                      api_key=api_key,
                                                      api_secret=api_secret).df.to_json()
    return my_json


@app.get("/strategy/bollinger-band/between-dates/{ticker_symbol}/{interval}/{start_date}/{end_date}")
def get_bollinger_band_strategy(ticker_symbol: str, interval: str, start_date: str, end_date: str, request: Request):
    api_key = request.headers.get('api_key')
    api_secret = request.headers.get('api_secret')
    my_json = strategies.bollinger_band.BollingerBand(ticker=ticker_symbol, interval=interval,
                                                      lookback_time=Constants.NO_LOOKBACK_TIME,
                                                      start_date=start_date, end_date=end_date, api_key=api_key,
                                                      api_secret=api_secret).df.to_json()
    return my_json


@app.get("/strategy/mean-reversion/lookback/{ticker_symbol}/{interval}/{lookback}")
def get_bollinger_band_strategy(ticker_symbol: str, interval: str, lookback: str, request: Request):
    api_key = request.headers.get('api_key')
    api_secret = request.headers.get('api_secret')
    my_json = strategies.mean_reversion.MeanReversion(ticker=ticker_symbol, interval=interval,
                                                      lookback_time=lookback, start_date=Constants.NO_START_DATE,
                                                      end_date=Constants.NO_END_DATE,
                                                      api_key=api_key,
                                                      api_secret=api_secret).df.to_json()
    return my_json


@app.get("/strategy/mean-reversion/between-dates/{ticker_symbol}/{interval}/{start_date}/{end_date}")
def get_bollinger_band_strategy(ticker_symbol: str, interval: str, start_date: str, end_date: str, request: Request):
    api_key = request.headers.get('api_key')
    api_secret = request.headers.get('api_secret')
    my_json = strategies.mean_reversion.MeanReversion(ticker=ticker_symbol, interval=interval,
                                                      lookback_time=Constants.NO_LOOKBACK_TIME,
                                                      start_date=start_date, end_date=end_date, api_key=api_key,
                                                      api_secret=api_secret).df.to_json()
    return my_json


@app.get("/strategy/stoch-rsi-macd/lookback/{ticker_symbol}/{interval}/{lookback}")
def get_bollinger_band_strategy(ticker_symbol: str, interval: str, lookback: str, request: Request):
    api_key = request.headers.get('api_key')
    api_secret = request.headers.get('api_secret')
    my_json = strategies.stoch_RSI_MACD.StochRSIMACD(ticker=ticker_symbol, interval=interval,
                                                     lookback_time=lookback, start_date=Constants.NO_START_DATE,
                                                     end_date=Constants.NO_END_DATE,
                                                     api_key=api_key,
                                                     api_secret=api_secret).df.to_json()
    return my_json


@app.get("/strategy/stoch-rsi-macd/between-dates/{ticker_symbol}/{interval}/{start_date}/{end_date}")
def get_bollinger_band_strategy(ticker_symbol: str, interval: str, start_date: str, end_date: str, request: Request):
    api_key = request.headers.get('api_key')
    api_secret = request.headers.get('api_secret')
    my_json = strategies.stoch_RSI_MACD.StochRSIMACD(ticker=ticker_symbol, interval=interval,
                                                     lookback_time=Constants.NO_LOOKBACK_TIME,
                                                     start_date=start_date, end_date=end_date, api_key=api_key,
                                                     api_secret=api_secret).df.to_json()
    return my_json
