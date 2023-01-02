import streamlit as st
import datetime
from backtesting.backtest import Backtest
from utils.constants import Constants
from utils.utility_methods import create_strategy_instance_from_string, validateInputs, get_strategy_class_names


class BacktestUI:
    """
    Use this class to encapsulate the attributes and functionalities for this UI page
    """

    def __init__(self, p_current_strategy_name, p_ticker_symbol, p_interval, p_lookback_time, p_start_date, p_end_date):
        self.current_strategy_name = p_current_strategy_name
        self.ticker_symbol = p_ticker_symbol
        self.interval = p_interval
        self.lookback_time = p_lookback_time
        self.start_date = p_start_date
        self.end_date = p_end_date
        self.strategy = None

    def submit_form(self):
        if st.button('Submit'):
            error = validateInputs(ticker_symbol, interval)
            if error != "":
                st.error(error)
                return None
            else:
                st.write("The given inputs are correct please see the charts below: ")

                # st.write("currentStrategy: " + self.current_strategy_name)
                # st.write("ticker_symbol: " + self.ticker_symbol)
                # st.write("interval: " + self.interval)
                # st.write("lookBackHours: " + self.lookback_time)
                # st.write("startDate: " + self.start_date)
                # st.write("endDate: " + self.end_date)
                return "Good"

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


class_names = get_strategy_class_names()
class_names.insert(0, Constants.DEFAULT_STRATEGY_STR)
current_strategy_name = st.selectbox('Choose a predefined strategy', class_names)

if current_strategy_name == 'RegressionModels':
    st.write("Implementation is coming soon ...")
elif current_strategy_name != 'Choose':
    # retrieve inputs:
    ticker_symbol = st.text_input('Ticker symbol:', placeholder='ex. BTCUSDT, ETHUSDT, ADAUSDT, etc')
    interval = st.text_input('Candle chart interval:', placeholder='ex. 15m, 30m, 1h, 4h, 6h, 24h')
    retrieve_method = st.radio('Choose data retrieval method: lookback hours or date range: ',
                               ('lookback', 'dateRange'))
    lookback_time = Constants.NO_LOOKBACK_TIME
    start_date = Constants.NO_START_DATE
    end_date = Constants.NO_END_DATE
    if retrieve_method == 'lookback':
        lookback_time = st.slider('Look back period in hours: ', 1, 300, 24)
        st.write(f'You have chosen: {str(lookback_time // 24)} days and {str(lookback_time % 24)}  hours')
        lookback_time = f'{str(lookback_time)} hours'
    elif retrieve_method == 'dateRange':
        appointment = st.slider("Select Range", min_value=datetime.date(2020, 12, 18), max_value=datetime.date.today(),
                                value=(datetime.date(2021, 4, 12), datetime.date(2022, 6, 12)))
        start_date = str(appointment[0])
        end_date = str(appointment[1])

    backTestUI = BacktestUI(current_strategy_name, ticker_symbol, interval, lookback_time, start_date, end_date)

    if backTestUI.submit_form() is not None:
        with st.spinner('Wait for it...'):
            backTestUI.retrieve_strategy_object()
        if backTestUI.strategy is not None:
            backTestUI.draw()
