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
       
         token_result_index = (parser["alert"]["exchange_token_result_index"]).split(',') 
         for i in range(0, len(token_result_index)):
             InitConfig.Alert.exchange_token_result_index.append(int(token_result_index[i]))
                  
         exchange_token = (parser["alert"]["exchange_token"]).split(',')        
         if exchange_token:              
               for i in range(0, len(exchange_token)):
                    InitConfig.Alert.exchange_token.append(int(exchange_token[i]))
                    InitConfig.Alert.exchange_token_all.append(int(exchange_token[i]))
                
         InitConfig.Alert.nifty_index = int(parser["alert"]["nifty_index"])  
         InitConfig.Alert.bank_nifty_index = int(parser["alert"]["bank_nifty_index"])  
         
         InitConfig.Trade_Data.enable_entry_rule_for =(parser["trade"]["enable_entry_rule_for"]).split(',') 
         InitConfig.Trade_Data.enable_exit_rule_that_contains =(parser["trade"]["enable_exit_rule_that_contains"]).split(',') 
         InitConfig.Trade_Data.skip_exit_rule_for =(parser["trade"]["skip_exit_rule_for"]).split(',') 

         return InitConfig   

    @staticmethod
    def get(parser: configparser.ConfigParser, section:str, key:str):        
         try:
            return parser[section][key]              
         except:
            return ""       