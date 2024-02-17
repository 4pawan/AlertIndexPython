from .smartConnect import SmartConnect
from .connect_util import ConnectUtil as cu
import pyotp
import datetime
import logging
from .result import Result
from .settings import Configuration as config
from .datetime_util import DateTimeUtility as dtu
from .notify_user import NotifyUser
from .telegram_util import TelegramUtility as tu
from .index_alert_util import IndexAlert 
from .stock_alert_util import StockAlert 

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')
    
    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    connect = SmartConnect(config.api_key)
    totp = pyotp.TOTP(config.token).now()
    data = connect.generateSession(config.username, config.pwd, totp)
    #tu.send_telegram_message(data)
    if data['status'] == False:
        tu.send_telegram_message(str(data), config.telegram_index_alert_token, config.telegram_index_alert_chat_id)
    else:     
        dt_now = dtu.get_ist_datetime_now()
        prev_day = dtu.subtract_minute(dtu.get_ist_previous_working_day(), 16)
        fromdate = dtu.to_ist_datetime_string(prev_day)
        todate = dtu.to_ist_datetime_string(dt_now)  
        live_data = connect.getMarketData("FULL", {"NSE": ["99926000", "99926009", "467"]})['data']['fetched']        
        IndexAlert.send_index_alert(live_data[1],live_data[2])
        stock_raw_data = cu.get_history_data_15min(connect ,fromdate, todate,"467")       
        stock_result = StockAlert.get_result(stock_raw_data,live_data[0],todate)
        NotifyUser.send_message(stock_result)
