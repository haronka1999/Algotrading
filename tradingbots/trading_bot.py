"""
--------------------  Revision History: ----------------------------------------
# 2022-11-22    -   Class created
# 2022-12-07    -   Class implemented
--------------------------------------------------------------------------------
Video: https://www.youtube.com/watch?v=X50-c54BWV8&t=53s - bot
        https://www.youtube.com/watch?v=VoDTVOJR3Og&t=52s - simulation of trading (no money)
Description:
Using the Strategy from strategies/STOCHRSIMACD.py

STOP LOSS : the  x% of buying price (99.5%)
Target Profit the x% of the buying price  (100.5%)
---------------------------------------------------------------------------
"""
import sqlalchemy as db
import time
from binance import Client
from binance.exceptions import BinanceAPIException
from utils.utility_methods import create_strategy_instance_from_string, get_strategy_class_names
from strategies.stoch_RSI_MACD import StochRSIMACD
import streamlit as st


# class_names = get_strategy_class_names()

class TradingBot:

    def __init__(self, pair, chosen_strategy, quantity, interval, lookback_time, public_key, private_key):
        # variables initialization
        self.public_key = public_key
        self.pair = pair
        self.private_key = private_key
        self.quantity = float(quantity)
        self.chosen_strategy = chosen_strategy
        self.client = Client(public_key, private_key)
        self.account = self.client.get_account()
        self.strategy = create_strategy_instance_from_string(chosen_strategy, pair, interval,
                                                             lookback_time, 'noStartDate', 'noEndDate', api_key=public_key,
                                                             api_secret=private_key)

        # variables validation
        self.error_message = self.validate_inputs()
        if self.error_message.strip() != "":
            print(self.error_message)
            return
        #order = self.client.create_order(symbol=pair, side='BUY', type='MARKET', quantity=10)
        print(self.client.get_symbol_info("HNTUSDT"))
        #print(order)
        # # initialize trading bot
        # while True:
        #     self.apply_strategy(pair, 0.0001)
        #     time.sleep(0.5)

    def apply_strategy(self, pair, qty, open_position=False):
        buy_price = 0
        self.refreshData()
        my_string = f'current close is: ' + str(self.strategy.df.Close.iloc[-1])
        st.write(my_string)
        print(f'current close is: ' + str(self.strategy.df.Close.iloc[-1]))
        # rowsFOrBuy = self.strategy.getBuyDatesForTradingBot()
        # print(rowsFOrBuy)
        if self.strategy.df.Buy.iloc[-1]:
            try:
                order = self.client.create_order(symbol=pair, side='BUY', type='MARKET', quantity=qty)
                print(order)
            except BinanceAPIException as e:
                print(e)
                return
            buy_price = float(order['fills'][0]['price'])
            open_position = True
        while open_position:
            time.sleep(0.5)
            self.refreshData()
            print(f'current close is: ' + str(self.strategy.df.Close.iloc[-1]))
            print(f'Target price is: ' + str(buy_price * 1.005))
            print(f'current Stop is: ' + str(buy_price * 0.998))
            if self.strategy.df.Close[-1] <= buy_price * 0.995 or self.strategy.df.Close[-1] >= 1.005 * buy_price:
                try:
                    order = self.client.create_order(symbol=pair, side='SELL', type='MARKET', quantity=qty)
                    print(order)
                    break
                except BinanceAPIException as e:
                    print(e)
                    return

    def refreshData(self):
        self.strategy = StochRSIMACD(self.pair, '1m', '10 min', 'noStartDate', 'noEndDate',
                                     api_key="public", api_secret="private")

    def check_quantity(self):
        info = self.client.get_symbol_info(self.pair)
        min_quantity = float(info["filters"][2]["minNotional"])
        if self.quantity < min_quantity:
            return f"The quantity provided is not enough. The minimum amount in USD is: {min_quantity}"
        return ""

    def check_strategy_exists(self):
        if self.chosen_strategy not in class_names:
            return "Something wrong with the strategy Name"
        return ""

    def create_test_order(self):
        order_dict = self.client.create_test_order(symbol=self.pair, side='BUY', type='MARKET', quantity=self.quantity)
        if not order_dict:
            return ""
        else:
            return str(order_dict)

    def validate_inputs(self):
        error_message = ""
        error_message += self.check_strategy_exists() + "\n"
        error_message += self.check_quantity() + "\n"
        error_message += self.create_test_order() + "\n"
        return error_message


engine = db.create_engine("sqlite:///test.db")
metadata = db.MetaData()
print(metadata.tables.keys())

# test = TradingBot("BTCBUSD", "StochRSIMACD", 10, "1m", '1000 min', api_key, api_secret)
