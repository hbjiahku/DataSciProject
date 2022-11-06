from constant import *
from dev.market_data import get_historical_price
from dev.market_data import stock_info


def md_download_hist_price(ticket, start_date, end_date, source="auto"):
    '''
    download market data from internet
    :param ticket: stock symbol (e.g. AAPL, AMZN)
    :param start_date: start date in datetime or excel date
    :param end_date:  start date in datetime or excel date
    :param source: auto/yfinance
    :return: pd.DataFrame
    '''
    return get_historical_price.download_hist_price(ticket, start_date, end_date, source)


def md_get_hist_price(ticket, start_date, end_date, source="auto"):
    '''
    get historical price from internet (yfinace) or local data (SQL/CSV)
    :param ticket: stock symbol (e.g. AAPL, AMZN)
    :param start_date: start date in datetime or excel date
    :param end_date:  start date in datetime or excel date
    :param source: auto(default: SQL)/yfinance/SQL/CSV
    :return: pd.DataFrame
    '''
    return get_historical_price.get_hist_price(ticket, start_date, end_date, source)


def md_save_hist_price(ticket, start_date, end_date, souece="auto", db_type=SQL):
    '''
    save histical price to database
    :param ticket: stock symbol (e.g. AAPL, AMZN)
    :param start_date: start date in datetime or excel date
    :param end_date:  start date in datetime or excel date
    :param souece: auto(yfinace)/yfinace
    :param db_type: SQL/CSV
    :return: None
    '''
    return get_historical_price.save_hist_price(ticket, start_date, end_date, souece, db_type)


def md_update_hist_price(ticket, start_date, end_date, souece="auto", db_type=SQL):
    '''update the historical price in database.
    :param ticket: stock symbol (e.g. AAPL, AMZN)
    :param start_date: start date in datetime or excel date
    :param end_date:  start date in datetime or excel date
    :param souece: auto(yfinace)/yfinace
    :param db_type: SQL/CSV
    :return: None
    '''
    return get_historical_price.update_hist_price(ticket, start_date, end_date, souece, db_type)


def md_get_sp_comp_stocks_info(rtype=PD_DATAFRAME):
    '''get the S&P 500 component stock information from wikipedia
    :param type: pd.DataFrame/dict
    :return: table contains all information about S&P 500 components
    '''
    return stock_info.get_sp_comp_stocks_info(rtype)
