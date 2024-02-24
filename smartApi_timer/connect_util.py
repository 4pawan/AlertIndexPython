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
    
    @staticmethod
    def place_order(connect: SmartConnect, tradingsymbol: str, symboltoken, transactiontype, price, quantity, ordertag):
        exchange = "NSE" if tradingsymbol.lower().endswith("eq") else "NFO"
        producttype = "CARRYFORWARD"
        place_order_param = {
            "variety": "NORMAL",
            "tradingsymbol": tradingsymbol,
            "symboltoken": symboltoken,
            "transactiontype": transactiontype,
            "exchange": exchange,
            "ordertype": "MARKET",
            "producttype": producttype,
            "duration": "DAY",
            #"price": price,
            #"squareoff": "0",
            #"stoploss": "0",
            "quantity": quantity,
            "ordertag": ordertag
        }
        return connect.placeOrder(place_order_param)

    @staticmethod
    def get_position(connect: SmartConnect):
        return connect.position()

    @staticmethod
    def get_order_details(connect: SmartConnect):
        return connect.orderBook()

    @staticmethod
    def get_ltp(connect: SmartConnect, symboltoken):
        return connect.ltpData("NSE", "", symboltoken)
