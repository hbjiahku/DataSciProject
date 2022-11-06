import datetime
from dateutil.relativedelta import relativedelta
import math

LOCAL_TZINFO = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
LOCAL_TIMEZONE = LOCAL_TZINFO.utcoffset(None)

XL_REF = datetime.datetime(1899, 12, 30, tzinfo=None)


def get_timezone():
    if LOCAL_TIMEZONE > datetime.timedelta(0, 18000):
        tzone = "APAC"
    elif LOCAL_TIMEZONE < -datetime.timedelta(0, 18000):
        tzone = "US"
    else:
        tzone = "EU"
    return tzone


def date_to_xl(d, xl_format=r"%d/%m/%Y"):
    if isinstance(d, str):
        d = datetime.datetime.strptime(d, xl_format)
    elif isinstance(d, datetime.date) and not isinstance(d, datetime.datetime):
        dargs = d.timetuple()[:6]
        d = datetime.datetime(*dargs)
    if d is None:
        return d
    d = d.replace(tzinfo=None)
    delta = d - XL_REF
    return float(delta.days) + float(delta.seconds) / 86400


def xl_to_date(x):
    d, s = math.modf(x)
    return datetime.datetime(1899, 12, 30) + datetime.timedelta(days=d, seconds=s * 86400)


def xltoday(with_time=False):
    if with_time:
        return date_to_xl(datetime.datetime.today())
    else:
        return date_to_xl(datetime.date.today())


def now():
    return datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')


def add_period(d, period, nb_period=1):
    dd, ww, mm, yy = (0, 0, 0, 0)
    if isinstance(d, int) or isinstance(d, float):
        d = xl_to_date(d)
    nb_period = int(period[:-1]) * nb_period
    if period[-1] == "D":
        dd = nb_period
    elif period[-1] == "W":
        ww = nb_period
    elif period[-1] == "M":
        mm = nb_period
    elif period[-1] == "Y":
        yy = nb_period
    return d + relativedelta(days=dd, weeks=ww, months=mm, years=yy)


if __name__ == "__main__":
    today = xltoday()
    print(xl_to_date(today))
    print(add_period(today, "1D"))
    print(add_period(today, "1W"))
    print(add_period(today, "1M"))
    print(add_period(today, "1Y"))
