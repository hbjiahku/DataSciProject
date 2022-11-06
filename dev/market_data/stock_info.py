import bs4 as bs
import pandas as pd
import requests
from constant import *


def get_sp_comp_stocks_info(rtype=PD_DATAFRAME):
    # 'https: // en.wikipedia.org / wiki / S % 26P_100'
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    header = [ele.text.replace('\n', '') for ele in table.findAll('tr')[0] if ele.text != '\n']
    sp_comp_stocks_dict = {coln: [] for coln in header}
    for row in table.findAll('tr')[1:]:
        for ix, ele in enumerate(row.findAll('td')):
            if ix == 2:
                sp_comp_stocks_dict[header[ix]].append(ele.next.attrs["href"])
            else:
                sp_comp_stocks_dict[header[ix]].append(ele.text.replace('\n', ''))
    if rtype == PD_DATAFRAME:
        return pd.DataFrame(sp_comp_stocks_dict)
    else:
        return sp_comp_stocks_dict
