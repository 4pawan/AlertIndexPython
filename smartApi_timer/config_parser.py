from .settings import Configuration as config
import configparser
from .init_configuation import  InitConfig, EntryData

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
       
         token_result_index_temp = (parser["alert"]["exchange_token_result_index"]).split(',') 
         for i in token_result_index_temp:
             InitConfig.Alert.exchange_token_result_index.append(int(i))
                  
         exchange_token_temp = (parser["alert"]["exchange_token"]).split(',')        
         if exchange_token_temp:              
               for i in exchange_token_temp:
                    InitConfig.Alert.exchange_token.append(int(i))
                    InitConfig.Alert.exchange_token_all.append(int(i))
                
         InitConfig.Alert.nifty_index = int(parser["alert"]["nifty_index"])  
         InitConfig.Alert.bank_nifty_index = int(parser["alert"]["bank_nifty_index"]) 

         InitConfig.Trade_Data.enable_trade = True if parser["trade"]["enable_trade"] == 'true' else False 

         entry_rules = (parser["trade"]["enable_entry_rule_for"]).split(',') 
         for rule in entry_rules: 
             param = rule.split('-')
             entry = EntryData
             entry.result_to_follow = int(param[0])
             entry.quantity = int(param[1])
             entry.order_type = param[2]
             entry.symbol_id = int(param[3]) 
             entry.symbol_name = param[4]                           
             InitConfig.Trade_Data.enable_entry_rule_for.append(entry)

         InitConfig.Trade_Data.enable_exit_rule_that_contains =(parser["trade"]["enable_exit_rule_that_contains"]).split(',') 
         InitConfig.Trade_Data.skip_exit_rule_for =(parser["trade"]["skip_exit_rule_for"]).split(',') 

         return InitConfig   

    @staticmethod
    def get(parser: configparser.ConfigParser, section:str, key:str):        
         try:
            return parser[section][key]              
         except:
            return ""       