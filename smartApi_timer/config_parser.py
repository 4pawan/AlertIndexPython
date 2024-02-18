from .settings import Configuration as config
import configparser
from .init_configuation import  InitConfig

class ConfigParserUtility:
    
    @staticmethod
    def configure():
         parser = configparser.ConfigParser()
         init_config = config.get_setting_from_url()
         parser.read_string(init_config)
         return parser

    @staticmethod
    def read_all_settings():   
         parser = ConfigParserUtility.configure()        
         InitConfig.App.debug = True if parser["app"]["debug"] == 'true' else False  
         InitConfig.Nse_Data.holiday_list =parser["nse"]["holiday_list"] 
         return InitConfig   

    @staticmethod
    def get(parser: configparser.ConfigParser, section:str, key:str):        
         try:
            return parser[section][key]              
         except:
            return ""       