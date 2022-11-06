import dash
from dash import html

from client.start_client import pyfunc_caller
from constant import *

dash.register_page(__name__)
colors = {
    'background': BG_COLOR,
    'text': TXT_COLOR
}
def generate_table(dataframe, max_rows=1000):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


layout = html.Div(
    style={"backgroundColor": colors["background"]},
    children=[
        html.H4(children='S&P 500 Component Stocks'),
        generate_table(pyfunc_caller().pd_md_get_sp_comp_stocks_info(PD_DATAFRAME))
    ]
)

