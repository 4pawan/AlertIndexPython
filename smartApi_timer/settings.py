import requests 
class Configuration:       
    api_key = 'xxxxxxxxx'
    username = 'xxxxxxxxxx'
    pwd = 'xxxxxxxx'
    token = "xxxxxxxxxxxxxxxxxx"
    time_zone = "Asia/Kolkata"
    azure_storage_connection_string = "xxxxxxxxxxxxxxxxx"
    telegram_token = "xxxxxxxxxxxxxxx"
    telegram_chat_id = -1xxxxxxxxxx
    telegram_index_alert_token = "xxxxxxxxxxxxxxx"
    telegram_index_alert_chat_id = -1xxxxxxxxxxxxxxx 
    setting_url =  "https://xxxxxxxxxx"


    @staticmethod
    def get_setting_from_url():          
         response_data =  requests.get(Configuration.setting_url) 
         return response_data.text 
    
    @staticmethod
    def unique(mylist):          
         return list(set(mylist))
