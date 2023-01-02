import time
import datetime
from binance import Client
from utils.constants import  Constants
from utils.utility_methods import create_strategy_instance_from_string, get_strategy_class_names
import streamlit as st
import csv

class_names = get_strategy_class_names()


class SimulateTradingBot:
    def __init__(self, pair, chosen_strategy, quantity, interval, lookback_time, public_key="", private_key=""):
        # variables initialization
        self.public_key = public_key
        self.pair = pair
        self.private_key = private_key
        self.usd_amount = float(quantity)
        self.chosen_strategy = chosen_strategy
        self.client = Client(public_key, private_key)
        # self.account = self.client.get_account()
        self.interval = interval
        self.lookback_time = lookback_time
        self.strategy = self.get_fresh_data()
        self.error_message = self.validate_inputs()
        # create the csv file for the trade output
        f = open('trades.csv', 'w')
        self.writer = csv.writer(f)
        self.writer.writerow(Constants.TRADE_OUTPUT_HEADER)

        if self.error_message.strip() != "":
            print(self.error_message)
            return
        # print(self.client.get_symbol_info("HNTUSDT"))

        # initialize trading bot
        # print("Trading Strategy initialized in 3 ...")
        # time.sleep(1)
        # print("2 ...")
        # time.sleep(1)
        # print("1 ...")
        # time.sleep(1)
        # print("Go .. !!!")
        while True:
            self.apply_strategy()
            time.sleep(0.5)

    def apply_strategy(self, open_position=False):
        buy_price = 0
        self.strategy = self.get_fresh_data()
        st.dataframe(self.strategy.df)
        st.write(f'current close is: ' + str(self.strategy.df.Close.iloc[-1]))
        print(f'current close is: ' + str(self.strategy.df.Close.iloc[-1]))
        if self.strategy.df.Buy.iloc[-1]:
            print("Position OPEN")
            buy_price = self.strategy.df.Open[-1]
            self.write_toCSV(side="BUY")
            open_position = True

        while open_position:
            time.sleep(0.5)
            self.strategy = self.get_fresh_data()
            print(f'current close is: ' + str(self.strategy.df.Close.iloc[-1]))
            print(f'Target price is: ' + str(buy_price * 1.005))
            print(f'current Stop is: ' + str(buy_price * 0.998))
            if self.strategy.df.Close[-1] <= buy_price * 0.995 or self.strategy.df.Close[-1] >= 1.005 * buy_price:
                print("Position CLOSED")
                self.write_toCSV(side="SELL")
                open_position = False

    def get_fresh_data(self):
        st.write(self.chosen_strategy)
        st.write(self.pair)
        st.write(self.interval)
        st.write(self.lookback_time)
        return create_strategy_instance_from_string(self.chosen_strategy, self.pair, self.interval,
                                                    self.lookback_time, 'noStartDate', 'noEndDate',
                                                    api_key=self.public_key,
                                                    api_secret=self.private_key)

    def create_test_order(self):
        order_dict = self.client.create_test_order(symbol=self.pair, side='BUY', type='MARKET',
                                                   quantity=self.usd_amount)
        if not order_dict:
            return ""
        else:
            return str(order_dict)

    # Helper functions
    # ---------------

    def check_quantity(self):
        info = self.client.get_symbol_info(self.pair)
        min_quantity = float(info["filters"][2]["minNotional"])
        if self.usd_amount < min_quantity:
            return f"The quantity provided is not enough. The minimum amount in USD is: {min_quantity}"
        return ""

    def validate_inputs(self):
        error_message = ""
        error_message += self.check_strategy_exists() + "\n"
        error_message += self.check_quantity() + "\n"
        # error_message += self.create_test_order() + "\n"
        return error_message

    def check_strategy_exists(self):
        if self.chosen_strategy not in class_names:
            return "Something wrong with the strategy Name"
        return ""

    def get_quantity(self):
        """
        Calculate the amount of the crypto is being bought from the price and the USD amount invested
        :return: how many cryptocurrency is being bought
        """
        return self.usd_amount / self.strategy.df.Open.iloc[-1]

    def write_toCSV(self, side):
        curr_time = datetime.datetime.now()
        symbol = self.pair
        price = self.strategy.df.Open.iloc[-1]
        quantity = self.get_quantity()
        usd_amount = self.usd_amount
        self.writer.writerow([curr_time, symbol, price, quantity, usd_amount, side])


test = SimulateTradingBot("BTCBUSD", "MeanReversion", 10, "1m", "50m")
