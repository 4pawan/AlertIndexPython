class InitConfig:
    
    class App:
        debug = False 
                                           
    class Nse_Data:
        holiday_list = ''
    
    class Alert:
        exchange_token = []   
        exchange_token_result_index = []
        exchange_token_all = [99926000, 99926009]   
        nifty_index = -1
        bank_nifty_index = -1

    class Trade_Data:
       enable_entry_rule_for =[]
       enable_exit_rule_that_contains = []
       skip_exit_rule_for = []