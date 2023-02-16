import datetime

from dateutil.relativedelta import relativedelta


def str_to_time(value):
    return datetime.time.fromisoformat("%H:%M")


def str_to_date(value, format="%Y-%m-%d"):
    if value is None:
        return None
    return datetime.datetime.strptime(value, format).date()


def str_to_datetime(value, format="%Y-%m-%d %H:%M:%S"):
    if value is None:
        return None
    return datetime.datetime.strptime(value, format)


def format_to_date_number(dt: datetime.datetime) -> int:
    """
    将时间格式化成int整数，如 20221212
    :param dt:
    """
    return int(dt.strftime("%Y%m%d"))


def timestamp_to_datetime(value, unit="ms"):
    unit = 1000 if unit == 'ms' else 1
    return datetime.datetime.fromtimestamp(value / unit)


def format_time_delta(seconds):
    if seconds is None:
        return None
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h:
        return f'{h:d}小时{m:d}分{s:d}秒'
    elif m:
        return f'{m:d}分{s:d}秒'
    else:
        return f'{s:d}秒'


def first_day_of_pre_month(dt: datetime.datetime):
    """
    获取上一个月的第一天
    """
    return (dt.replace(day=1) - datetime.timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0)


def first_day_of_month(dt: datetime.datetime) -> datetime.datetime:
    return dt.replace(day=1)


def last_day_of_month(any_day: datetime.datetime):
    """
    根据任何时间获取同月的最后一天
    return: datetime.datetime
    """
    return (any_day + relativedelta(day=31)).replace(hour=23, minute=59, second=59)


def first_day_fo_pre_week(dt: datetime.datetime) -> datetime.datetime:
    """
    获取上周的第一天
    """
    return first_day_of_week(dt) - datetime.timedelta(days=7)


def first_day_of_week(dt: datetime.datetime) -> datetime.datetime:
    """
    获取当天所在周的第一天
    """
    return dt - datetime.timedelta(days=dt.weekday())


def last_day_of_week(dt: datetime.datetime) -> datetime.datetime:
    """
    获取当天所在周的第一天
    """
    return dt + datetime.timedelta(days=6 - dt.weekday())

def days_of_month(year, month):
    """
    获取指定月份的天数
    """
    from calendar import monthrange
    num_days = monthrange(year, month)[1]
    return num_days


def ceil_day(d: datetime.datetime) -> datetime.datetime:
    """
    获取指定时间的当天的最后时刻
    :param d:
    :return:
    """
    return d.replace(hour=23, minute=59, second=59, microsecond=9999)


def floor_day(d: datetime.datetime) -> datetime.datetime:
    """
   获取指定时间的当天的开始时刻
   :param d:
   :return:
   """
    return d.replace(hour=0, minute=0, second=0, microsecond=0)
