import pandas as pd
from datetime import datetime
import yfinance as yf

from time_helper import xltoday, add_period, xl_to_date, date_to_xl
from tools import math_tool
from database.sql_db import SQLEngine
from database.csv_db import CSVEngine
from constant import *

SRC_MAP = {
    "auto": "yfinance",
    "yfinance": "yfinance"
}


def download_hist_price_from_yfinance(ticket, start_date: datetime, end_date: datetime):
    data = yf.download(ticket, start=start_date,
                       end=end_date)
    col = ["Date"] + [cn for cn in data.columns]
    data["Date"] = [date_to_xl(d) for d in data.index]  # reset index to excel date
    data.index = range(len(data.index))
    return data[col]


def download_hist_price(ticket, start_date, end_date, source="auto"):
    '''download the historical data from internet source
    :param ticket:
    :param start_date:
    :param end_date:
    :param source:
    :return: historical price with xl date as index
    '''
    if math_tool.is_num(start_date):
        start_date = xl_to_date(float(start_date))
    if math_tool.is_num(end_date):
        end_date = xl_to_date(float(end_date))
    source = source.lower()
    direct_src = SRC_MAP[source]
    if direct_src == "yfinance":
        data = download_hist_price_from_yfinance(ticket, start_date, end_date)
    else:
        data = download_hist_price_from_yfinance(ticket, start_date, end_date)
        # TODO: Add data validation
    return data


def save_hist_price(ticket, start_date, end_date, souece="auto", db_type=SQL):
    hist_price = download_hist_price(ticket, start_date, end_date, souece)

    if db_type == CSV:
        s = CSVEngine()
    else:
        s = SQLEngine()
    s.save(ticket, hist_price)


def update_hist_price(ticket, start_date, end_date, souece="auto", db_type=SQL):
    if not math_tool.is_num(start_date):
        start_date = date_to_xl(start_date)
    if not math_tool.is_num(end_date):
        end_date = date_to_xl(end_date)
    if db_type == CSV:
        s = CSVEngine()
    else:
        s = SQLEngine()
    try:
        hist_price = s.read(tbl_name=ticket, data_type=PD_DATAFRAME)
        col = list(hist_price.columns)
        if hist_price["Date"].iloc[0] > start_date:
            hist_price_added = download_hist_price(ticket, start_date, hist_price["Date"].iloc[0])
            hist_price = pd.concat([hist_price_added, hist_price])[col]
        if hist_price["Date"].iloc[-1] < end_date:
            hist_price_added = download_hist_price(ticket, hist_price["Date"].iloc[-1], end_date)
            hist_price = pd.concat([hist_price, hist_price_added])[col]
        hist_price.index = range(len(hist_price.index))
        s.save(ticket, hist_price)
    except:
        save_hist_price(ticket, start_date, end_date, souece, db_type)


def get_hist_price(ticket, start_date, end_date, source="auto"):
    if not math_tool.is_num(start_date):
        start_date = date_to_xl(start_date)
    if not math_tool.is_num(end_date):
        end_date = date_to_xl(end_date)
    if source == "auto":
        source = SQL
    if source == SQL:
        s = SQLEngine()
    elif source == CSV:
        s = CSVEngine()
    else:
        return download_hist_price(ticket, start_date, end_date, source)
    hist_price = s.read(tbl_name=ticket, data_type=PD_DATAFRAME)
    return hist_price[(hist_price["Date"] >= start_date) & (hist_price["Date"] <= end_date)]


if __name__ == "__main__":
    today = xltoday()
    today_dt = today - 200
    ticket = "AAPL"
    save_hist_price(ticket, start_date=add_period(today_dt, "1Y", -1), end_date=today_dt, souece="auto", db_type=SQL)
    price = get_hist_price(ticket, start_date=add_period(today_dt, "1Y", -1), end_date=today_dt, source=SQL)
    print(price)
    update_hist_price(ticket, start_date=add_period(today_dt, "2Y", -1), end_date=today_dt + 100, souece="auto",
                      db_type=SQL)
    price = get_hist_price(ticket, start_date=add_period(today_dt, "2Y", -1), end_date=today_dt + 100, source=SQL)
    print(price)
