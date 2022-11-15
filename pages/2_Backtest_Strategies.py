"""
--------------------  Revision History: ----------------------------------------
* 2022-10-15    -   Class Created
--------------------------------------------------------------------------------
Version Number: 1.0 V
Description:

    The use should be able to choose an existing strategy and backtest it in multiple timeframes
"""

import streamlit as st
import datetime
from utils.inputValidation import validateInputs

ticker_symbol = ""
interval = ""
lookBackHours = ""
startDate = ""
endDate = ""

option = st.selectbox(
    'Choose a predefined strategy',
    ('Choose', 'Bollinger Bands', 'Mean Reversion', 'Roll Max Roll Min'))

if option != 'Choose':
    # retrieve inputs:
    ticker_symbol = st.text_input('Ticker symbol:', placeholder='ex. BTCUSD, ETHUSDT, ADAUSDT, etc')
    interval = st.text_input('Chandle chart interval:', placeholder='ex. 15m, 30m, 1h, 4h, 6h, 24h')

    retrieveMethod = st.radio('Choose data retrieval method: lookback hours or date range: ', ('lookback', 'dateRange'))
    if retrieveMethod == 'lookback':
        lookBackHours = st.slider('Look back period in hours: ', 1, 300, 24)
        st.write('You have choosed:', str(lookBackHours // 24 ) + ' days and ' + str(lookBackHours % 24 ) + " hours" )
    elif retrieveMethod == 'dateRange':
        st.markdown("<h3 style='text-align: center'>or</h3>", unsafe_allow_html=True)
        appointment = st.slider("Select Range", min_value=datetime.date(2020, 12, 18), max_value=datetime.date.today(),
                                value=(datetime.date(2021, 4, 12), datetime.date(2022, 6, 12)))
        startDate = str(appointment[0])
        endDate = str(appointment[1])

    if st.button('Submit'):
        error = validateInputs(ticker_symbol, interval, lookBackHours, startDate, endDate)
        if error != "":
            st.write(error)
        else:
            st.write("The given inputs are correct please see the charts below: ")
