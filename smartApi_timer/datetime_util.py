from datetime import datetime, timedelta
from pandas.tseries.offsets import BDay as bd
import pytz
from .settings import Configuration as config
from .init_configuation import InitConfig
class DateTimeUtility:

    @staticmethod
    def get_ist_datetime_now():
        return datetime.now(pytz.timezone(config.time_zone))

    @staticmethod
    def get_ist_previous_working_day(initConfig_data: InitConfig):
        dt_now = datetime.now(pytz.timezone(config.time_zone))
        prev_bd = dt_now-bd(1)      
        dates_list = initConfig_data.Nse_Data.holiday_list .split(',')                
        for d in dates_list:
            if d == prev_bd.strftime("%d-%m-%Y"):
                prev_bd = prev_bd - bd(1)
                break                 
        return prev_bd

    @staticmethod
    def subtract_minute(dt: datetime, minute: int):
        return dt - timedelta(minutes=minute)

    @staticmethod
    def to_ist_date_string(dt: datetime):
        return dt.strftime('%Y_%m_%d')

    @staticmethod
    def to_ist_datetime_string(dt: datetime):
        return dt.strftime('%Y-%m-%d %H:%M')
