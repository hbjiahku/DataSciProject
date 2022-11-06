from client.rest_proxy import funct_call
def pd_md_download_hist_price(ticket=None,start_date=None,end_date=None,source="auto"):
	"""None"""
	return funct_call("md_download_hist_price",ticket=ticket,start_date=start_date,end_date=end_date,source=source)

# This is debug file.
