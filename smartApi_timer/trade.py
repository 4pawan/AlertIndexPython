from .connect_util import ConnectUtil as cu
from .init_configuation import InitConfig
from .smartConnect import SmartConnect
from .debug_app import Debug_App
from datetime import datetime
from .result import Result
import pandas as pd


class Trade:

    @staticmethod
    def get_orders(connect: SmartConnect):
        return cu.get_order_details(connect)["data"]

    @staticmethod
    def enter_or_exit_trade(connect: SmartConnect, init_data: InitConfig, result: Result):

        if datetime.now().time() < datetime.time(3, 45): #9.15am ist
            Debug_App.debug(init_data.App.debug, f"existing..before 3.45am UTC")
            return
               
        positions = cu.get_position(connect)["data"]
        orders = cu.get_order_details(connect)["data"]
        is_entry_taken = Trade.take_entry(connect, init_data, positions, orders, result)
        is_exit_taken = Trade.square_off_position(connect, init_data, positions, orders, result)


    @staticmethod
    def take_entry(connect, init_data: InitConfig, positions, orders, result: Result):   
         
        df_positions = pd.DataFrame(positions)
        df_orders = pd.DataFrame(orders)        
        entry_data = init_data.Trade_Data.enable_entry_rule_for
              
        for data in entry_data:               
            pos_found = pd.DataFrame()
            order_found = pd.DataFrame()  
            order_type_to_execute = "b" if data.order_type.lower() == "buy" else "s"
            
            if not df_positions.empty:           
                filter_symbol_condition = df_positions["tradingsymbol"] == data.symbol_id               
                pos_found = df_positions[filter_symbol_condition]

            if not df_orders.empty:           
                filter_order_symbol_condition = df_orders["tradingsymbol"] == data.symbol_id  
                filter_order_status_condition = df_orders["orderstatus"] == "open"  
                order_found = df_orders[filter_order_symbol_condition & filter_order_status_condition]
                        
            is_market_view_satisfied = result.Symbol_token == data.result_to_follow and result.Signal == order_type_to_execute   
            Debug_App.debug(init_data.App.debug, f"take_entry1:{pos_found} {order_found} {is_market_view_satisfied}")         
            
            if pos_found is None and order_found is None and is_market_view_satisfied:                
                ltp_data = cu.get_ltp(connect, data.symbol_name ,data.symbol_id)['data']
                Debug_App.debug(init_data.App.debug, f"take_entry2.1:{ltp_data}")
                ltp = float(ltp_data['ltp'])
                Debug_App.debug(init_data.App.debug, f"take_entry2.2:{ltp_data['tradingsymbol']} {data.symbol_id} {str(data.order_type).upper()} {ltp} {data.quantity}")
                status = cu.place_order(connect, ltp_data["tradingsymbol"], data.symbol_id, str(data.order_type).upper(), ltp, data.quantity, f"robot :{result.Signal}{result.Strength}")
                Debug_App.debug(init_data.App.debug, f"take_entry:{status}")
                Debug_App.debug(True, f"entry order placed with param {ltp_data['tradingsymbol']} {data.order_type} {data.quantity} {ltp}")
                return True
                
        return False


    @staticmethod
    def square_off_position(connect: SmartConnect, init_data: InitConfig, positions, orders, result: Result):
        positions = cu.get_position(connect)["data"]
        orders = cu.get_order_details(connect)["data"]
        df_order = pd.DataFrame(orders)
        existing_order_found = pd.DataFrame()  
        for pos in positions:           
            transaction_type = "BUY" if pos["buyqty"] == "0" else "SELL"
            if not df_order.empty: 
                filter_symbol_condition = df_order["tradingsymbol"] == pos["tradingsymbol"]
                filter_transaction_condition = df_order["transactiontype"] == transaction_type
                filter_order_status_condition = df_order["orderstatus"] == "open" 
                existing_order_found = df_order[filter_symbol_condition & filter_transaction_condition & filter_order_status_condition]
            required_square_off_signal = Trade.extract_market_view_to_square_off_from_position(pos)
            is_valid_result = str(pos["tradingsymbol"]).lower() in result.Symbol_Name.lower()
            is_rev_market_found = required_square_off_signal == Result.Signal and is_valid_result and Result.Strength > 1
            Debug_App.debug(init_data.App.debug, f"square_off_1:{existing_order_found} {is_rev_market_found} {is_valid_result}")

            if existing_order_found is None and is_rev_market_found and is_valid_result:
                ltp_data = cu.get_ltp(connect, pos["tradingsymbol"], pos['symboltoken'])['data']
                ltp = float(ltp_data['ltp'])
                Debug_App.debug(init_data.App.debug, f"square_off_2:{pos} {transaction_type} {ltp}") 
                status = cu.place_order(connect, pos["tradingsymbol"], pos["symboltoken"], transaction_type, ltp, pos["netqty"], f"robot :{result.Signal}{result.Strength}")
                Debug_App.debug(init_data.App.debug, f"square_off_3:{status}")
                Debug_App.debug(True, f"exit order placed with param {ltp_data['tradingsymbol']} {transaction_type} {pos['netqty']} {ltp}")
                return True            
        
        return False

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
