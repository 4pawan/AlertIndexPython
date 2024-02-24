from .config_parser import ConfigParserUtility as cfu
from .datetime_util import DateTimeUtility as dtu
from .telegram_util import TelegramUtility as tu
from .settings import Configuration as config
from .connect_util import ConnectUtil as cu
from .index_alert_util import IndexAlert 
from .stock_alert_util import StockAlert 
from .smartConnect import SmartConnect
from .notify_user import NotifyUser
from .debug_app import Debug_App
import azure.functions as func
from .result import Result
from .trade import Trade
import datetime
import logging
import pyotp


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')
    
    logging.info('Python timer trigger function ran at %s', utc_timestamp)    
    init_data = cfu.read_all_settings()
    debug_enable = init_data.App.debug

    connect = SmartConnect(config.api_key)
    totp = pyotp.TOTP(config.token).now()
    data = connect.generateSession(config.username, config.pwd, totp)
    Debug_App.debug(debug_enable,data)
    if debug_enable == True:
        orders = Trade.get_orders(connect)
        Debug_App.debug(debug_enable, f"0: {orders}") 

    if data['status'] == False:
        tu.send_telegram_message(str(data), config.telegram_index_alert_token, config.telegram_index_alert_chat_id)
    else:     
        dt_now = dtu.get_ist_datetime_now()
        prev_day = dtu.subtract_minute(dtu.get_ist_previous_working_day(init_data), 16)
        fromdate = dtu.to_ist_datetime_string(prev_day)
        todate = dtu.to_ist_datetime_string(dt_now)  
        Debug_App.debug(debug_enable, f"2: {fromdate}_{todate}")               
        live_data = connect.getMarketData("FULL", {"NSE": init_data.Alert.exchange_token_all })['data']['fetched']   
        Debug_App.debug(debug_enable, f"3: {live_data}")     
        IndexAlert.send_index_alert(live_data[init_data.Alert.nifty_index],live_data[init_data.Alert.bank_nifty_index])
 
        for i in range(0, len(init_data.Alert.exchange_token)):
            stock_raw_data = cu.get_history_data_15min(connect ,fromdate, todate, init_data.Alert.exchange_token[i])  
            Debug_App.debug(debug_enable, f"4_{i}: {stock_raw_data}") 
            result_index = init_data.Alert.exchange_token_result_index[i]     
            stock_result = StockAlert.get_result(stock_raw_data,live_data[result_index],todate)
            Debug_App.debug(debug_enable, f"5_{i}: {stock_result.Close}")  
            NotifyUser.send_message(stock_result)
