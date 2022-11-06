import pandas as pd

from config.config_helper import get_config, DATA_SRC_CFG, SQL_SOURCE
from constant import *


class SQLMeta:
    def __init__(self):
        self.sql_src = SQL_SOURCE

    def connection(self):
        raise NotImplementedError

    def execute(self, sql=None):
        raise NotImplementedError


if SQL_SOURCE == "sqlite3":
    import sqlite3


    class SQLEngine(SQLMeta):
        def __init__(self):
            super().__init__()
            self.db_location = get_config(DATA_SRC_CFG)["database"]["sqlite3"]["db_address"]
            self.conn = sqlite3.connect(PROJECT_ROOT + self.db_location)

        def __del__(self):
            self.conn.close()

        def connection(self):
            return self.conn

        def execute(self, sql=None):
            with self.connection() as conn:
                rs = conn.cursor().execute(sql)
                conn.commit()
            return rs

        def save(self, tbl_name, data):
            if isinstance(data, pd.DataFrame):
                return self.save_df_to_db(tbl_name=tbl_name, df=data)
            else:
                NotImplementedError("SQLEngine doesn't have this data type")

        def read(self, tbl_name, data_type):
            if data_type == PD_DATAFRAME:
                return self.read_df_from_db(tbl_name=tbl_name)
            else:
                NotImplementedError("SQLEngine doesn't have this data type")

        def save_df_to_db(self, tbl_name, df):
            df.to_sql(tbl_name, con=self.conn, if_exists="replace")

        def read_df_from_db(self, tbl_name) -> pd.DataFrame:
            df = pd.read_sql_query(sql=f"SELECT * FROM {tbl_name}", con=self.conn)  # .reset_index()
            return df.set_index(df.columns[0])

else:
    from sqlalchemy import create_engine, Table, Column, MetaData


    class SQLConfig:
        HOST = get_config(DATA_SRC_CFG)["database"]["sql"]["host"]
        # database name, if you want just to connect to MySQL server, leave it empty
        DATABASE = "us_stock_price_db"
        # this is the user you create
        USER = get_config(DATA_SRC_CFG)["database"]["sql"]["user_name"]
        # user password
        PASSWORD = get_config(DATA_SRC_CFG)["database"]["sql"]["password"]


    class SQLEngine(SQLMeta):

        def __init__(self):
            super().__init__()
            self.__db_engine = create_engine(
                'mysql+pymysql://{}:{}@{}/{}'.format(SQLConfig.USER, SQLConfig.PASSWORD, SQLConfig.HOST,
                                                     SQLConfig.DATABASE))
            self.__conn = self.__db_engine.connect()

        def __del__(self):
            self.__conn.close()

        def connection(self):
            return self.__conn

        def execute(self, sql=None):
            with self.connection() as con:
                rs = con.execute(sql)
            return rs

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
    print(s)
    sql_engine = SQLEngine()
    sql_engine.save_to_db(ticket, s)
    df = sql_engine.read_from_db(ticket, PD_DATAFRAME)
    sql_engine.save_to_db(ticket, df)
    df2 = sql_engine.read_from_db(ticket, PD_DATAFRAME)
    print(df)
