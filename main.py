from time_helper import xltoday, xl_to_date, date_to_xl, add_period
from client.start_client import pyfunc_caller
from constant import *

if __name__ == "__main__":
    today = xltoday()
    today_dt = xl_to_date(today)
    start_date = date_to_xl(add_period(today_dt, "1Y", -1))
    end_date = date_to_xl(today_dt)
    s = pyfunc_caller().pd_md_download_hist_price(ticket="MSFT", start_date=start_date, end_date=end_date, source="auto")
    print(s)
    today = xltoday()
    today_dt = today - 200
    ticket = "AAPL"
    pyfunc_caller().pd_md_save_hist_price(ticket, start_date=add_period(today_dt, "1Y", -1), end_date=today_dt, souece="auto", db_type=SQL)
    price = pyfunc_caller().pd_md_get_hist_price(ticket, start_date=add_period(today_dt, "1Y", -1), end_date=today_dt, source=SQL)
    print(price)
    pyfunc_caller().pd_md_update_hist_price(ticket,  start_date=add_period(today_dt, "2Y", -1), end_date=today_dt + 100, souece="auto", db_type=SQL)
    price = pyfunc_caller().pd_md_get_hist_price(ticket, start_date=add_period(today_dt, "2Y", -1), end_date=today_dt + 100, source=SQL)
    print(price)
