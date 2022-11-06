import pandas as pd

from config.config_helper import get_config, DATA_SRC_CFG
from constant import *


class CSVEngine:
    def __init__(self):
        self.data_dir = get_config(DATA_SRC_CFG)["csv"]["directory"]

    def save(self, table_name, df: pd.DataFrame):
        df.to_csv(PROJECT_ROOT + self.data_dir + f"/{table_name}.csv")

    def read(self, table_name, data_type=PD_DATAFRAME) -> pd.DataFrame:
        if data_type == PD_DATAFRAME:
            return pd.read_csv(PROJECT_ROOT + self.data_dir + f"/{table_name}.csv", index_col=0)
        else:
            raise NotImplementedError("CSVEngine doesn't have this data type")


if __name__ == "__main__":
    from client.start_client import pyfunc_caller
    from time_helper import *

    ticket = "MSFT"
    today = xltoday()
    today_dt = xl_to_date(today)
    start_date = date_to_xl(add_period(today_dt, "1Y", -1))
    end_date = date_to_xl(today_dt)
    s = pyfunc_caller().pd_md_download_hist_price(ticket=ticket, start_date=start_date, end_date=end_date,
                                                  source="auto")
    csv_eg = CSVEngine()
    df = csv_eg.save(s, ticket)
    csv_eg.read(ticket)
    print(df)