from .smartConnect import SmartConnect


class ConnectUtil:
        
    @staticmethod
    def get_history_data_15min(connect : SmartConnect, fromdate, todate, stock_id):
        hist = {
        "exchange": "NSE",
        "symboltoken": stock_id,
        "interval": "FIFTEEN_MINUTE",
        "fromdate": fromdate, #"2024-02-15 11:00",
        "todate": todate  #"2024-02-16 11:16"
         }
        return connect.getCandleData(hist)
    