from .telegram_util import TelegramUtility as tu
from .settings import Configuration as config


class Debug_App:
    
    @staticmethod
    def debug(enable: bool, message):
         if enable:
            tu.send_telegram_message(str(message), config.telegram_index_alert_token, config.telegram_index_alert_chat_id)

