import pandas as pd
from .result import Result
from .blob_util import BlobUtility as bu
from .telegram_util import TelegramUtility as tu
from .analysis import Analysis


class StockAlert:

    @staticmethod
    def get_result(hist_data, live_data, todate):
        if hist_data['data'] is None:
            return None
    
        df = pd.DataFrame(hist_data['data'])
        Result.Change = live_data['netChange']
        Result.OI = live_data['opnInterest'] / 100000
        vol_data = live_data['tradeVolume'] / 100000
        Result.Vol = float("{:.2f}".format(vol_data))    
        Result.Close = live_data['ltp']
        Result.Date = todate
        Result.Symbol_token = live_data['symbolToken']
        Result.Symbol_Name = live_data['tradingSymbol']        
        df = Analysis.generate_signal(df)
        Result.Strength = Analysis.get_moving_avg_strength(df)
        Result.Signal = df.iloc[0]['signal']
        rsi_data = 0 if df.iloc[-1]['rsi'] is None else df.iloc[-1]['rsi']
        Result.Rsi = float("{:.2f}".format(rsi_data))
        return Result
        