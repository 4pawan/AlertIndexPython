import requests 
class Configuration:       
    api_key = 'XXXXXXXX'
    username = 'XXXXXX'
    pwd = 'XXXXXX'
    token = "XXXXXXXXXXX"
    time_zone = "Asia/Kolkata"
    azure_storage_connection_string = "XXXXXXXXXXXXXXX"
    telegram_token = "XXXXXXXXXXXXXXXX"
    telegram_chat_id = -1XXXXXXXX
    telegram_index_alert_token = "XXXXXXXXXXXXXXXXX"
    telegram_index_alert_chat_id = -1XXXXXXXXXXX 
    setting_url =  "XXXXXXXXXXXXXXXXXX"


    @staticmethod
    def get_setting_from_url():          
         response_data =  requests.get(Configuration.setting_url) 
         return response_data.text 
