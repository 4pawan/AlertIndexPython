from .telegram_util import TelegramUtility as tu
from .settings import Configuration as config

class IndexAlert:

    @staticmethod
    def send_index_alert(nifty50, banknifty):        
        nifty_50 = float(nifty50['netChange'])
        bank_nifty = float(banknifty['netChange'])
        is_nifty_triggered =  nifty_50 > 100 or nifty_50 < -100
        is_bank_nifty_triggered =  bank_nifty > 300 or bank_nifty < -300
        is_condition_triggered = is_nifty_triggered or is_bank_nifty_triggered
        message = f"Welcome {nifty_50}   {bank_nifty}"
        if is_condition_triggered:
             tu.send_telegram_message(message,config.telegram_index_alert_token, config.telegram_index_alert_chat_id)
   