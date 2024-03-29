from .result import Result
from .blob_util import BlobUtility as bu
from .telegram_util import TelegramUtility as tu
from .settings import Configuration as config

class NotifyUser:
           
    @staticmethod
    def send_message(data: Result):
          message = ''
          if not (data is None):
              strgth = f"<b>{data.Strength}</b>" if data.Strength == 0 else data.Strength  
              mv_diff = float("{:.2f}".format(data.Mv9-data.Mv26))      
              tu.send_telegram_message(f"{data.Signal}{strgth}  {data.Change}  close {data.Close} oi  {data.OI}   vol {data.Vol}  rsi {data.Rsi} {mv_diff}",config.telegram_token,config.telegram_chat_id)
              message = f"{data.Date}|{data.Signal}|{data.Strength}|{data.Close}|{data.Change}|{data.OI}|{data.Vol}|{data.Rsi}|"
              bu.add_logging_to_azure_blob(message+"\n")
          else:
              tu.send_telegram_message(f"None...",config.telegram_token,config.telegram_chat_id)    
