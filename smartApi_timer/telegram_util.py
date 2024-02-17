import requests 
from .settings import Configuration as config


class TelegramUtility:
    
    @staticmethod
    def send_telegram_message(message : str,token: str, chat_id):
           url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
           requests.get(url)