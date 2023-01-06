import time
import datetime
from binance import Client
from binance.exceptions import BinanceAPIException
from utils.constants import Constants
from utils.utility_methods import create_strategy_instance_from_string
import csv

class TradingBot:
    def __init__(self, pair, chosen_strategy, quantity, interval, public_key="", private_key="", is_simulation=True):
        # variables initialization
        self.buy_price = 0
        self.public_key = public_key
        self.pair = pair
        self.private_key = private_key
        self.usd_amount = float(quantity)
        self.chosen_strategy = chosen_strategy
        self.client = Client(public_key, private_key)
        self.is_simulation = is_simulation
        self.interval = interval
        # this parameter shouldn't be predefined by the user since the strategy is highly dependent on the correct amount
        self.lookback_time = Constants.LOOKBACK_TIME_FOR_BOTS
        self.strategy = self.get_fresh_data()
        self.error_message = self.validate_inputs()
        # create the csv file for the trade output
        f = open('trades.csv', 'w')
        self.writer = csv.writer(f)
        self.writer.writerow(Constants.TRADE_OUTPUT_HEADER)

        if self.error_message.strip() != "":
            print(self.error_message)
            return

        while True:
            self.apply_strategy()
            time.sleep(1)

    def apply_strategy(self, open_position=False):
        self.buy_price = 0
        self.strategy = self.get_fresh_data()
        print(f'current close is: ' + str(self.strategy.df.Close.iloc[-1]))
        if self.strategy.df.Buy.iloc[-1]:
            print("Position OPEN")
            self.create_order(side="BUY")
            open_position = True
        while open_position:
            time.sleep(1)
            self.strategy = self.get_fresh_data()
            print(f'current close is: ' + str(self.strategy.df.Close.iloc[-1]))
            print(f'Target price is: ' + str(self.buy_price * 1.005))
            print(f'current Stop is: ' + str(self.buy_price * 0.998))
            if self.strategy.df.Sell.iloc[-1]:
                print("Position CLOSED")
                self.create_order(side="SELL")
                open_position = False

    def get_fresh_data(self):
        return create_strategy_instance_from_string(self.chosen_strategy, self.pair, self.interval,
                                                    self.lookback_time, Constants.NO_START_DATE, Constants.NO_END_DATE,
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
        error_message += self.check_quantity() + "\n"
        return error_message


    def get_quantity(self):
        """
        Calculate the amount of the crypto is being bought from the price and the USD amount invested
        :return: how many cryptocurrency are being bought
        """
        return self.usd_amount / self.strategy.df.Open.iloc[-1]

    def write_toCSV(self, side):
        curr_time = datetime.datetime.now()
        symbol = self.pair
        price = self.strategy.df.Open.iloc[-1]
        quantity = self.get_quantity()
        usd_amount = self.usd_amount
        self.writer.writerow([curr_time, symbol, price, quantity, usd_amount, side])

    def create_order(self, side):
        if self.is_simulation:
            self.write_toCSV(side)
            self.buy_price = self.strategy.df.Open[-1]
        else:
            try:
                order = self.client.create_order(symbol=self.pair, side=side, type='MARKET', quantity=self.get_quantity())
                print(order)
            except BinanceAPIException as e:
                print(e)
                return
            self.buy_price = float(order['fills'][0]['price'])



#test = TradingBot("AXSBUSD", "MeanReversion", 10, "1m", is_simulation=True)
