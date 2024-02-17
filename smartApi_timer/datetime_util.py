from datetime import datetime, timedelta
from pandas.tseries.offsets import BDay as bd
import pytz
from .settings import Configuration as config

class DateTimeUtility:

    @staticmethod
    def get_ist_datetime_now():
        return datetime.now(pytz.timezone(config.time_zone))

    @staticmethod
    def get_ist_previous_working_day():
        dt_now = datetime.now(pytz.timezone(config.time_zone))
        return (dt_now -bd())

    @staticmethod
    def subtract_minute(dt: datetime, minute: int):
        return dt - timedelta(minutes=minute)

    @staticmethod
    def to_ist_date_string(dt: datetime):
        return dt.strftime('%Y_%m_%d')

    @staticmethod
    def to_ist_datetime_string(dt: datetime):
        return dt.strftime('%Y-%m-%d %H:%M')
