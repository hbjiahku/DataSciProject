import dash
from dash import dcc
from dash import html

from constant import *
dash.register_page(__name__, path='/')

colors = {
    'background': BG_COLOR,
    'text': TXT_COLOR
}

layout = html.Div(
    children=[
        dcc.Markdown('''
        ### This is home page.
        '''),
    ])
