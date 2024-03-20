import pandas as pd
import pandas_ta as ta
from .indicator import Indicator

class Analysis:

    @staticmethod
    def generate_signal(df):
        ema9 = df[4].ewm(span=9, adjust=False).mean()
        ema26 = df[4].ewm(span=26, adjust=False).mean()
        mv = ta.above(ema26, ema9)
        if mv.iloc[-1] == 1:
            df['mv'] = mv
            df['rsi'] = Indicator.calc_rsi(df[4])
            df['signal'] = 's'
            df['mv9'] = ema9
            df['mv26'] = ema26
            return df
        else:
            return Analysis.generate_buyer_signal(df)

    @staticmethod
    def generate_buyer_signal(df):
        ema9 = df[4].ewm(span=9, adjust=False).mean()
        ema26 = df[4].ewm(span=26, adjust=False).mean()
        df['mv'] = ta.above(ema9, ema26)
        df['rsi'] = Indicator.calc_rsi(df[4])
        df['signal'] = 'b'
        df['mv9'] = ema9
        df['mv26'] = ema26        
        return df

    @staticmethod
    def get_moving_avg_strength(df):
        rev = df.iloc[::-1]
        strength = 0
        for i in range(0, len(rev)):
            strength += rev.iloc[i]['mv']
            if rev.iloc[i]['mv'] == 0:
                break
        return strength
