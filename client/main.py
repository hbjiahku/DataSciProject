from client.start_client import pyfunc_caller

if __name__ == "__main__":
    from time_helper import xltoday, xl_to_date, add_period, date_to_xl

    today = xltoday()
    today_dt = xl_to_date(today)
    start_date = date_to_xl(add_period(today_dt, "1Y", -1))
    end_date = date_to_xl(today_dt)
    s = pyfunc_caller().pd_md_download_hist_price(ticket="MSFT", start_date=start_date, end_date=end_date,
                                                  source="auto")
    print(s)
