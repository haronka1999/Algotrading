"""
--------------------  Revision History: ----------------------------------------
* 2022-10-15    -   File Created
# 2022-11-24    -   Implementation started
# 2022-12-07    -   Implementation done:
                    -  the UI is working (only tested on STOCHMACDRSI
--------------------------------------------------------------------------------
Description:

This code is responsible for displaying the UI for launching Bots
"""

import streamlit as st
from tradingbots.trading_bot import TradingBot
from utils import constants
from utils.Utilities import getStrategyClassNames

# GLOBAL VARIABLES
ticker_symbol = ""
interval = ""
classNames = getStrategyClassNames()
classNames.insert(0, constants.default_strategy_str)
currentStrategy = st.selectbox('Choose a predefined strategy', help="Choose", options=classNames)

st.write("The current strategies are working: STOCHRSI")
if currentStrategy != constants.default_strategy_str:
    # retrieve inputs:
    ticker_symbol = st.text_input('Ticker symbol:', placeholder='ex. BTCBUSD, ETHBUSD, ADABUSD, etc')
    interval = st.text_input('Candle chart interval:', placeholder='ex.1m, 5m, 15m, 30m, 1h, 4h etc.')
    quantity = st.number_input('Choose the amount of USD dollars to be invested:')
    public_key = st.text_input('Please enter your Binance Public Key')
    private_key = st.text_input('Please enter your Binance Private Key')

    if st.button('Submit'):
        strategy = TradingBot(ticker_symbol, currentStrategy, quantity, interval,
                              constants.lookback_time_for_bots, public_key, private_key)
