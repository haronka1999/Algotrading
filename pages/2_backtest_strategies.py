"""
--------------------  Revision History: ----------------------------------------
* 2022-10-15    -   File Created
* 2022-10-16    -   Strategies connected to UI, the ability to display date in the SCREEN
* 2022-11-24    -   helper functions moved to ui_utils
--------------------------------------------------------------------------------
Description:

    The use should be able to choose an existing strategy and backtest it in multiple timeframes
"""

import streamlit as st
import datetime
from pages.utils_ui.utils import create_strategy_instance_from_string, validateInputs
from utils.utilities import get_strategy_class_names
from utils.constants import no_start_date, no_end_date, no_lookback_time

# GLOBAL VARIABLES
ticker_symbol = ""
interval = ""
lookback_time = no_lookback_time
start_date = no_start_date
end_date = no_end_date
class_names = get_strategy_class_names()
current_strategy = st.selectbox('Choose a predefined strategy', class_names)


# create an instance for every strategy based on the chosen string

def submitFormAndGetStrategy():
    if st.button('Submit'):
        error = validateInputs(ticker_symbol, interval)
        if error != "":
            st.write(error)
            return None
        else:
            st.write("The given inputs are correct please see the charts below: ")
            st.write("We got the following input:")

            st.write("currentStrategy: " + current_strategy)
            st.write("ticker_symbol: " + ticker_symbol)
            st.write("interval: " + interval)
            st.write("lookBackHours: " + lookback_time)
            st.write("startDate: " + start_date)
            st.write("endDate: " + end_date)
            p_strategy = create_strategy_instance_from_string(current_strategy, ticker_symbol, interval, lookback_time, start_date, end_date)
            if p_strategy is None:
                st.write("Something wrong with the strategy option")
                return None
            else:
                return p_strategy


st.write("The current strategies are working: BollingerBand")
if current_strategy != 'Choose':
    # retrieve inputs:
    ticker_symbol = st.text_input('Ticker symbol:', placeholder='ex. BTCUSD, ETHUSDT, ADAUSDT, etc')
    interval = st.text_input('Chandle chart interval:', placeholder='ex. 15m, 30m, 1h, 4h, 6h, 24h')
    retrieve_method = st.radio('Choose data retrieval method: lookback hours or date range: ', ('lookback', 'dateRange'))

    if retrieve_method == 'lookback':
        lookback_time = st.slider('Look back period in hours: ', 1, 300, 24)
        st.write('You have choosed:', str(lookback_time // 24) + ' days and ' + str(lookback_time % 24) + " hours")
        lookback_time = str(lookback_time) + " hours"
    elif retrieve_method == 'dateRange':
        st.markdown("<h3 style='text-align: center'>or</h3>", unsafe_allow_html=True)
        appointment = st.slider("Select Range", min_value=datetime.date(2020, 12, 18), max_value=datetime.date.today(),
                                value=(datetime.date(2021, 4, 12), datetime.date(2022, 6, 12)))
        start_date = str(appointment[0])
        end_date = str(appointment[1])

    # TODO correct the plotting and actual trades needs to be debugged
    strategy = submitFormAndGetStrategy()
    if strategy is not None:
        st.pyplot(strategy.plot())
        st.markdown("Trades")
        st.dataframe(strategy.actual_trades)
        st.markdown("DataFrame")
        st.dataframe(strategy.df)


