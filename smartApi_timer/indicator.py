from talipp.indicators import EMA, SMA, RSI, ADX

class Indicator:

    @staticmethod
    def calc_rsi(prices, period=14):
        delta = prices.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
        avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        rsi_val = RSI(period=14, input_values=prices)
        return rsi_val

    @staticmethod
    def calc_adx(high, low, close):
        adx_data = ADX(high, low, close)
        return adx_data
