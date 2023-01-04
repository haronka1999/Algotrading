import os
import streamlit as st
import datetime
from backtesting.backtest import Backtest
from utils import utility_methods
from utils.constants import Constants
from utils.utility_methods import create_strategy_instance_from_string, get_strategy_class_names


class BacktestUI:
    """
    Use this class to encapsulate the attributes and functionalities for this UI page
    """

    def __init__(self):
        self.current_strategy_name = ""
        self.ticker_symbol = ""
        self.interval = ""
        self.retrieve_method = ""
        self.lookback_time = Constants.NO_LOOKBACK_TIME
        self.start_date = Constants.NO_START_DATE
        self.end_date = Constants.NO_END_DATE
        self.class_names = get_strategy_class_names(path=os.path.join("strategies"))
        self.class_names.insert(0, Constants.DEFAULT_STRATEGY_STR)
        self.strategy = None


    def retrieve_inputs(self):
        self.ticker_symbol = st.text_input('Ticker symbol:', placeholder='ex. BTCUSDT, ETHUSDT, ADAUSDT, etc')
        self.interval = st.text_input('Candle chart interval:', placeholder='ex. 15m, 30m, 1h, 4h, 6h, 24h')
        self.retrieve_method = st.radio('Choose data retrieval method: lookback hours or date range: ',
                                   ('lookback', 'dateRange'))


    def retrieve_strategy_object(self):
        self.strategy = create_strategy_instance_from_string(self.current_strategy_name, self.ticker_symbol,
                                                             self.interval,
                                                             self.lookback_time, self.start_date, self.end_date)
        if self.strategy is None:
            st.error("Something wrong with the strategy option")
            return None
        else:
            return self.strategy

    def draw(self):
        st.pyplot(self.strategy.plot())
        st.markdown("Trades")
        st.dataframe(self.strategy.actual_trades)
        backtest_values = Backtest(self.strategy)
        rel_returns = backtest_values.get_relative_returns()
        cum_returns_str = backtest_values.get_cumulative_returns()
        st.write("Relative returns")
        st.dataframe(rel_returns)
        st.write("Cumulative return is: " + cum_returns_str)
        st.markdown("DataFrame")
        st.dataframe(self.strategy.df)



backtestUI = BacktestUI()
current_strategy_name = st.selectbox('Choose a predefined strategy', backtestUI.class_names)
backtestUI.current_strategy_name = current_strategy_name

if current_strategy_name == 'RegressionModels':
    st.write("Implementation is coming soon ...")
elif current_strategy_name != Constants.DEFAULT_STRATEGY_STR:
    # retrieve inputs:
    backtestUI.retrieve_inputs()
    if backtestUI.retrieve_method == 'lookback':
        lookback_time = st.slider('Look back period in hours: ', 1, 300, 24)
        st.write(f'You have chosen: {str(lookback_time // 24)} days and {str(lookback_time % 24)}  hours')
        lookback_time = f'{str(lookback_time)} hours'
        backtestUI.lookback_time = lookback_time
    elif backtestUI.retrieve_method == 'dateRange':
        appointment = st.slider("Select Range", min_value=datetime.date(2020, 12, 18), max_value=datetime.date.today(),
                                value=(datetime.date(2021, 4, 12), datetime.date(2022, 6, 12)))
        start_date = str(appointment[0])
        end_date = str(appointment[1])
        backtestUI.start_date = start_date
        backtestUI.end_date = end_date

    if utility_methods.submit_form(backtestUI.ticker_symbol, backtestUI.interval) is not None:
        with st.spinner('Wait for it...'):
            backtestUI.retrieve_strategy_object()
        if backtestUI.strategy is not None:
            backtestUI.draw()
