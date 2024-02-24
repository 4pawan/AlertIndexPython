from datetime import datetime
from .smartConnect import SmartConnect
from .connect_util import ConnectUtil as cu
from .init_configuation import InitConfig
from .result import Result
import pandas as pd


class Trade:

    @staticmethod
    def get_orders(connect: SmartConnect):
        return cu.get_order_details(connect)["data"]

    @staticmethod
    def enter_or_exit_trade(connect: SmartConnect, symbol_name: str, order_type: str, quantity: int, result: Result):

        if datetime.now().time() < datetime.time(3, 45): #9.15am ist
            return

        print("Im not called..........................")

        all_position = cu.get_position(connect)["data"]
        orders = cu.get_order_details(connect)["data"]
        is_entry_taken = Trade.take_entry(connect, symbol_name, order_type, quantity, all_position, orders, Result)
        is_exit_taken = Trade.square_off_position(connect, result)



    @staticmethod
    def take_entry(connect, symbol_name, symboltoken, order_type: str, quantity, all_position, orders, Result):
        df_position = pd.DataFrame(all_position)
        df_order = pd.DataFrame(orders)
        filter_pos_entry_symbol_condition = df_position["tradingsymbol"] == symbol_name
        filter_order_entry_symbol_condition = df_order["tradingsymbol"] == symbol_name
        pos_entry_found = df_position[filter_pos_entry_symbol_condition]
        order_entry_found = df_order[filter_order_entry_symbol_condition]
        order_type_to_execute = "b" if order_type.lower() == "buy" else "s"
        is_fav_market_found = Result.Signal == order_type_to_execute
        if pos_entry_found is None and order_entry_found is None and is_fav_market_found:
            ltp_data = cu.get_ltp(connect, symbol_name, symboltoken)
            ltp = float(ltp_data['data']['ltp'])
            cu.place_order(connect, symbol_name, symboltoken, order_type, ltp, quantity, "test tag")
            return True

        return False

    @staticmethod
    def square_off_position(connect: SmartConnect, init_data: InitConfig, result: Result):
        all_position = cu.get_position(connect)["data"]
        orders = cu.get_order_details(connect)["data"]
        df_order = pd.DataFrame(orders)

        for pos in all_position:
            print('pos', pos)
            transaction_type = "BUY" if pos["buyqty"] == "0" else "SELL"
            filter_symbol_condition = df_order["tradingsymbol"] == pos["tradingsymbol"]
            filter_transaction_condition = df_order["transactiontype"] == transaction_type
            order_found = df_order[filter_transaction_condition and filter_symbol_condition]
            required_square_off_signal = Trade.extract_market_view_to_square_off_from_position(pos)
            is_rev_market_found = required_square_off_signal == Result.Signal and Result.Strength > 2
            if order_found is None and is_rev_market_found:
               cu.place_order(connect, pos["tradingsymbol"], pos["symboltoken"], transaction_type, 0.0, pos["netqty"], "test tag")

    @staticmethod
    def extract_market_view_to_square_off_from_position(pos):
        order_trans_type = ""
        if pos["buyqty"] == "0":
            order_trans_type = "SELL"
        if pos["sellqty"] == "0":
            order_trans_type = "BUY"
        order_name = str(pos["tradingsymbol"])
        if order_name.endswith("CE") and order_trans_type == "BUY":
            return "s"
        if order_name.endswith("CE") and order_trans_type == "SELL":
            return "b"
        if order_name.endswith("PE") and order_trans_type == "BUY":
            return "b"
        if order_name.endswith("PE") and order_trans_type == "SELL":
            return "s"
        if order_name.endswith("FUT") and order_trans_type == "BUY":
            return "s"
        if order_name.endswith("FUT") and order_trans_type == "SELL":
            return "b"
        if order_name.endswith("EQ") and order_trans_type == "BUY":
            return "s"
        if order_name.endswith("EQ") and order_trans_type == "SELL":
            return "b"
        return "0"
