"""
Use this script to access the Trading functionality (simulation and real)
"""
import os
import sys
import time

from binance import Client

from utils.utility_methods import get_strategy_class_names

class_names = get_strategy_class_names(path=os.path.join("strategies"))


def validate_number(number):
    try:
        number = int(number)
    except ValueError:
        print("error input - type conversion")
        sys.exit()
    return number


def get_simulation():
    print(
        " --- Please Choose if you want to trade with real money or just simulation ---\n1 - Simulation\n2 - Real Money")
    input_str = input(">> Your selection: ")
    simulation_nmb = validate_number(input_str)
    print(f"--> You have selected: {simulation_nmb}")
    if simulation_nmb != 1 and simulation_nmb != 2:
        print("Error input - selecting trading type")
        sys.exit()
    return simulation_nmb


def get_strategy():
    class_name_dict = {key + 1: item for key, item in enumerate(class_names)}
    print("--- Choose one of the Strategy below: ---")
    for key in class_name_dict:
        print(f"\t{key} - {class_name_dict[key]}")
    input_str = input(">> Your selection: ")
    strategy_nmb = validate_number(input_str)
    if strategy_nmb < 1 or strategy_nmb > len(class_name_dict):
        print("Error input")
        sys.exit()
    print(f"--> You have selected {class_name_dict[strategy_nmb]}\n")
    return {class_name_dict[strategy_nmb]}


def get_pair():
    print("--- Insert crypto the pair which you would like to trade. ---\n"
          "--- Please keep the convention presented in the below line: ---\n--- Examples: BTCUSDT, ETHBUSD, SOLUSDC, etc. ---")
    p_pair = input(">> Your selection: ").strip()
    print()
    symbol_info = Client().get_symbol_info(p_pair)
    if symbol_info is None:
        print("The given pair is not existing in Binance")
        sys.exit()
    return p_pair


def get_amount(p_pair):
    print("--- Please insert how much money should you invest by each trade: ---")
    p_amount = input(">> Your selection: ")
    try:
        p_amount = float(p_amount)
    except ValueError:
        print("error input - type conversion")
        sys.exit()

    symbol_info = Client().get_symbol_info(p_pair)
    min_quantity = float(symbol_info["filters"][2]["minNotional"])
    if p_amount < min_quantity:
        print(f"The given amount is not enough. You should give at least {min_quantity} USD")
        sys.exit()
    print(f'--> You have chosen to trade with {p_amount} USD\n')
    return p_amount


def get_interval():
    interval_types = ["1m", "5m", "15m", "30m", "1h", "4h"]
    print(
        f"--- Please choose on what interval should data be pulled\n you can choose from the following list: {interval_types} ---")
    chosen_interval = input(">> Your selection: ")
    if chosen_interval not in interval_types:
        print("You have chosen wrong interval")
        sys.exit()
    return chosen_interval


def get_simulation_str():
    if simulation == 1:
        return "Simulation"
    elif simulation == 2:
        return "Real Money"
    else:
        return "Something is wrong"


def get_keys(p_simulation):
    public_k, private_k = "", ""
    if p_simulation == 2:
        print(" --- Please give your credentials to Binance")
        public_k = input(">> public key: ")
        private_k = input(">> private key: ")
    return public_k, private_k


print("\t\t\t<<<WELCOME IN OUR TRADING APP>>>")
print("<<<To launch your bot please provide the necessary inputs>>>\n")

pair = get_pair()
strategy = get_strategy()
amount = get_amount(pair)
interval = get_interval()
simulation = get_simulation()
public_key, private_key = get_keys(simulation)
simulation_str = get_simulation_str()

print("\n------------------------\n"
      "Please review your inputs:\n"
      f"\t- Currency pair: {pair}\n"
      f"\t- Strategy: {strategy}\n"
      f"\t- Amount in USD: {amount}\n"
      f"\t- Pulling interval: {interval}\n"
      f"\t- Trade type: {simulation_str} ")

input1 = input("Please review and press ENTER: ")
if input1 == "":
    print(f"Trading bot will be initialized in {time.sleep(1)} 3 ... {time.sleep(1)} 2... {time.sleep(1)}  1... ")
else:
    print("Program closed")
    sys.exit()
