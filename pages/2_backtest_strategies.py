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
from pages.utils_ui.utils import createStrategyInstanceFromString, validateInputs
from utils.constants import COLUMN_LIST
from utils.Utilities import getStrategyClassNames
from utils.constants import noStartDate, noEndDate, noLookBackHours

# GLOBAL VARIABLES
ticker_symbol = ""
interval = ""
lookBackHours = noLookBackHours
startDate = noStartDate
endDate = noEndDate
classNames = getStrategyClassNames()
currentStrategy = st.selectbox('Choose a predefined strategy', classNames)


# create an instance for every strategy based on the chosen string

def submitFormAndGetStrategy():
    if st.button('Submit'):
        error = validateInputs(ticker_symbol, interval, lookBackHours, startDate, endDate)
        if error != "":
            st.write(error)
        else:
            st.write("The given inputs are correct please see the charts below: ")
            st.write("We got the following input:")

            p_strategy = createStrategyInstanceFromString(currentStrategy, ticker_symbol, interval,
                                                          COLUMN_LIST, lookBackHours, startDate, endDate)
            if p_strategy is None:
                st.write("Something wrong with the strategy option")
            else:
                return p_strategy


st.write("The current strategies are working: BollingerBand")
if currentStrategy != 'Choose':
    # retrieve inputs:
    ticker_symbol = st.text_input('Ticker symbol:', placeholder='ex. BTCUSD, ETHUSDT, ADAUSDT, etc')
    interval = st.text_input('Chandle chart interval:', placeholder='ex. 15m, 30m, 1h, 4h, 6h, 24h')
    retrieveMethod = st.radio('Choose data retrieval method: lookback hours or date range: ', ('lookback', 'dateRange'))

    if retrieveMethod == 'lookback':
        lookBackHours = st.slider('Look back period in hours: ', 1, 300, 24)
        st.write('You have choosed:', str(lookBackHours // 24) + ' days and ' + str(lookBackHours % 24) + " hours")
        lookBackHours = str(lookBackHours)
    elif retrieveMethod == 'dateRange':
        st.markdown("<h3 style='text-align: center'>or</h3>", unsafe_allow_html=True)
        appointment = st.slider("Select Range", min_value=datetime.date(2020, 12, 18), max_value=datetime.date.today(),
                                value=(datetime.date(2021, 4, 12), datetime.date(2022, 6, 12)))
        startDate = str(appointment[0])
        endDate = str(appointment[1])

    strategy = submitFormAndGetStrategy()
    if strategy is not None:
        st.dataframe(strategy.df)
        fig = strategy.plot()
        st.pyplot(fig)
