import streamlit as st
from tradingbots.simulate_trading_bot import SimulateTradingBot
from utils.constants import Constants
from utils.utility_methods import get_strategy_class_names

class AppyStrategyUI:
    """
    Responsible for encapsulating and displaying the UI for launching trading Bots
    """

    def __init__(self):
        self.private_key = ""
        self.public_key = ""
        self.quantity = ""
        self.ticker_symbol = ""
        self.interval = ""
        self.class_names = get_strategy_class_names()
        self.class_names.insert(0, Constants.DEFAULT_STRATEGY_STR)

    def retrieve_inputs(self):
        self.ticker_symbol = st.text_input('Ticker symbol:', placeholder='ex. BTCBUSD, ETHBUSD, ADABUSD, etc')
        self.interval = st.text_input('Candle chart interval:', placeholder='ex.1m, 5m, 15m, 30m, 1h, 4h etc.')
        self.quantity = st.number_input('Choose the amount of USD dollars to be invested:')
        self.public_key = st.text_input('Please enter your Binance Public Key')
        self.private_key = st.text_input('Please enter your Binance Private Key')


applyUI = AppyStrategyUI()
current_strategy = st.selectbox('Choose a predefined strategy', help="Choose", options=applyUI.class_names)

st.write("The current strategies are working: STOCHRSI")
if current_strategy != Constants.DEFAULT_STRATEGY_STR:
    # retrieve inputs:
    applyUI.retrieve_inputs()
    if st.button('Submit'):
        strategy = SimulateTradingBot(applyUI.ticker_symbol, current_strategy, applyUI.quantity, applyUI.interval,
                                      Constants.LOOKBACK_TIME_FOR_BOTS, applyUI.public_key, applyUI.private_key)
