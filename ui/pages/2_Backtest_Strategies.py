"""
--------------------  Revision History: ----------------------------------------
* 2022-10-15    -   Class Created
--------------------------------------------------------------------------------
Version Number: 1.0 V
Description:

    The use should be able to choose an existing strategy and backtest it in multiple timeframes
"""
import streamlit as st



from utils.inputValidation import validateInputs
error = validateInputs("","","","","")
st.write(error)
# ticker_symbol = ""
# interval = ""
# lookBackHours = ""
# startDate = ""
# endDate = ""
# option = st.selectbox(
#     'Choose a predefined strategy',
#     ('Choose', 'Bollinger Bands', 'Mean Reversion', 'Roll Max Roll Min'))
#
# if option != 'Choose':
#     st.write('You selected:', option)
#     ticker_symbol = st.text_input( 'Ticker symbol:',placeholder= 'ex. BTCUSD, ETHUSDT, ADAUSDT, etc')
#     interval = st.text_input('Chandle chart interval:', 'ex. 15m, 30m, 1h, 4h, 6h, 24h')
#     st.write('The current movie title is', interval)
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         lookBackHours = st.slider('Look back period in hours: ', 0, 1000, 10)
#         st.write('Values:', lookBackHours)
#     with col2:
#         st.markdown("<h3 style='text-align: center'>or</h3>", unsafe_allow_html=True)
#     with col3:
#         startDate = st.date_input("Or choose a startdate")
#         st.write('Startdate is: ', startDate)
#         endDate = st.date_input("Choose and enddate")
#         st.write('Startdate is: ', endDate)
#
#
#
#
# if st.button('Say hello'):
#     error = validateInputs(ticker_symbol, interval, lookBackHours, startDate, endDate)
#     if error != "":
#         st.write(error)
#     else:
#         st.write("The given inputs are correct please see the charts below: ")
