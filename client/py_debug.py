from interface.interface import __funct_call


def pd_md_download_hist_price(ticket=None, start_date=None, end_date=None, source="auto"):
	"""download market data from internet
:param ticket: stock symbol (e.g. AAPL, AMZN)
:param start_date: start date in datetime or excel date
:param end_date:  start date in datetime or excel date
:param source: auto/yfinance
:return: pd.DataFrame"""
	import os
	print(os.getcwd())
	print(globals())
	return __funct_call("pd_md_download_hist_price", ticket=ticket, start_date=start_date, end_date=end_date, source=source)

def pd_md_get_hist_price(ticket=None, start_date=None, end_date=None, source="auto"):
	"""get historical price from internet (yfinace) or local data (SQL/CSV)
:param ticket: stock symbol (e.g. AAPL, AMZN)
:param start_date: start date in datetime or excel date
:param end_date:  start date in datetime or excel date
:param source: auto(default: SQL)/yfinance/SQL/CSV
:return: pd.DataFrame"""
	import os
	print(os.getcwd())
	print(globals())
	return __funct_call("pd_md_get_hist_price", ticket=ticket, start_date=start_date, end_date=end_date, source=source)

def pd_md_save_hist_price(ticket=None, start_date=None, end_date=None, souece="auto", db_type="SQL"):
	"""save histical price to database
:param ticket: stock symbol (e.g. AAPL, AMZN)
:param start_date: start date in datetime or excel date
:param end_date:  start date in datetime or excel date
:param souece: auto(yfinace)/yfinace
:param db_type: SQL/CSV
:return: None"""
	import os
	print(os.getcwd())
	print(globals())
	return __funct_call("pd_md_save_hist_price", ticket=ticket, start_date=start_date, end_date=end_date, souece=souece, db_type=db_type)

def pd_md_update_hist_price(ticket=None, start_date=None, end_date=None, souece="auto", db_type="SQL"):
	"""update the historical price in database.
:param ticket: stock symbol (e.g. AAPL, AMZN)
:param start_date: start date in datetime or excel date
:param end_date:  start date in datetime or excel date
:param souece: auto(yfinace)/yfinace
:param db_type: SQL/CSV
:return: None"""
	import os
	print(os.getcwd())
	print(globals())
	return __funct_call("pd_md_update_hist_price", ticket=ticket, start_date=start_date, end_date=end_date, souece=souece, db_type=db_type)

def pd_md_get_sp_comp_stocks_info(rtype="pd.DataFrame"):
	"""get the S&P 500 component stock information from wikipedia
:param type: pd.DataFrame/dict
:return: table contains all information about S&P 500 components"""
	import os
	print(os.getcwd())
	print(globals())
	return __funct_call("pd_md_get_sp_comp_stocks_info", rtype=rtype)

# This is debug file.
