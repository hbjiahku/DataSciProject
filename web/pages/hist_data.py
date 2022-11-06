# React Programming
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from stockstats import StockDataFrame as Sdf
from datetime import date

from time_helper import xltoday, add_period, xl_to_date, date_to_xl
from client.start_client import pyfunc_caller
from constant import *

dash.register_page(__name__)

sp_info = pyfunc_caller().pd_md_get_sp_comp_stocks_info("dict")

colors = {
    'background': BG_COLOR,
    'text': TXT_COLOR,
    'line': LINE_COLOR
}
layout = html.Div(style={'backgroundColor': colors['background']},
                  children=[
                      html.Div(
                          children=[
                              dbc.Row(
                                  children=[

                                      dbc.Col(children=[
                                          html.Header(
                                              children=[
                                                  html.H1(
                                                      "Stock Price",
                                                      style={
                                                          "textAlign": "center",
                                                          "color": colors["text"],
                                                      },
                                                  )
                                              ]
                                          )
                                      ]
                                      )
                                  ]
                              )
                          ]
                      ),
                      html.Br(),
                      html.Br(),
                      html.Br(),
                      html.Br(),
                      html.Div(
                          children=[
                              dbc.Row([
                                  dbc.Col(  # Tickers
                                      dcc.Dropdown(
                                          id="ticker",
                                          options=sp_info['Symbol'],
                                          searchable=True,
                                          value='AAPL',
                                          placeholder="enter stock name",
                                          style={
                                              'height': '18px',
                                          }
                                      ),
                                      width={"size": 3, "offset": 1},
                                  ),
                                  dbc.Col(  # Graph type
                                      dcc.Dropdown(
                                          id="chart",
                                          options=[
                                              {"label": "line", "value": "Line"},
                                              {"label": "candlestick", "value": "Candlestick"},
                                              {"label": "Simple moving average",
                                               "value": "SMA"},
                                              {
                                                  "label": "Exponential moving average",
                                                  "value": "EMA",
                                              },
                                              {"label": "MACD", "value": "MACD"},
                                              {"label": "RSI", "value": "RSI"},
                                              {"label": "OHLC", "value": "OHLC"},
                                          ],
                                          value="Line",
                                          style={
                                              'height': '18px',
                                              "color": "#000000"
                                          }
                                      ),
                                      width={"size": 3},
                                  ),
                                  dbc.Col(  # date range
                                      html.Div(
                                          dcc.DatePickerRange(
                                              id='date-range',
                                              min_date_allowed=date(1957, 8, 5),  # S&P 500 established
                                              max_date_allowed=xl_to_date(xltoday()).date(),
                                              start_date=add_period(xltoday(), '5Y', nb_period=-1).date(),
                                              end_date=xl_to_date(xltoday()).date(),
                                              display_format="DD/MM/YYYY",
                                              style={
                                                  "color": BG_COLOR,
                                                  'height': '18px',
                                                  'width': '300px',
                                              }
                                          ),
                                      ),
                                      width={"size": 3}
                                  ),
                                  dbc.Col(  # button
                                      dbc.Button(
                                          "Plot",
                                          id="submit-button-state",
                                          className="mr-1",
                                          n_clicks=1,
                                          color='success',
                                          style={"color": BLACK},
                                      ),
                                      width={"size": 2},
                                  ),
                              ]),
                          ]
                      ),
                      dcc.Graph(
                          id="time-series-chart",
                          config={
                              "displaylogo": False,
                              "modeBarButtonsToRemove": ["pan2d", "lasso2d"],
                          },
                      ),
                      # dcc.Input(id='start_date', value=add_period(xltoday(), '5Y', nb_period=-1)),
                      # dcc.Input(id='end_date', value=xl_to_date(xltoday())),
                  ], )


@callback(
    Output('time-series-chart', 'figure'),
    Input('submit-button-state', 'n_clicks'),
    State('ticker', 'value'),
    State('chart', 'value'),
    State('date-range', 'start_date'),
    State('date-range', 'end_date'))
def display_time_series(n_clicks, ticker, chart_name, start_date, end_date):
    start_date = date_to_xl(start_date, r"%Y-%m-%d")
    end_date = date_to_xl(end_date, r"%Y-%m-%d")
    pyfunc_caller().pd_md_update_hist_price(ticker, start_date, end_date, souece="auto", db_type=SQL)
    df = pyfunc_caller().pd_md_get_hist_price(ticker, start_date, end_date, source="auto")
    df.columns = [col.lower() for col in df.columns]
    df['date'] = [xl_to_date(d) for d in df['date']]
    stock = Sdf(df)
    if chart_name == "Candlestick":
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=list(df['date']),
                    open=list(df.open),
                    high=list(df.high),
                    low=list(df.low),
                    close=list(df.close),
                    name="Candlestick",
                )
            ],
            layout={
                "height": 1000,
                "title": chart_name,
                "showlegend": True,
                "plot_bgcolor": colors["background"],
                "paper_bgcolor": colors["background"],
                "font": {"color": colors["text"]},
            },
        )
    elif chart_name == "SMA":
        df.index = df.date
        close_ma_10 = df.close.rolling(10).mean()
        close_ma_15 = df.close.rolling(15).mean()
        close_ma_30 = df.close.rolling(30).mean()
        close_ma_100 = df.close.rolling(100).mean()
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=list(close_ma_10.index), y=list(close_ma_10), name="10 Days"
                ),
                go.Scatter(
                    x=list(close_ma_15.index), y=list(close_ma_15), name="15 Days"
                ),
                go.Scatter(
                    x=list(close_ma_30.index), y=list(close_ma_15), name="30 Days"
                ),
                go.Scatter(
                    x=list(close_ma_100.index), y=list(close_ma_15), name="100 Days"
                ),
            ],
            layout={
                "height": 1000,
                "title": chart_name,
                "showlegend": True,
                "plot_bgcolor": colors["background"],
                "paper_bgcolor": colors["background"],
                "font": {"color": colors["text"]},
            },
        )
    elif chart_name == "OHLC":
        fig = go.Figure(
            data=[
                go.Ohlc(
                    x=df.date,
                    open=df.open,
                    high=df.high,
                    low=df.low,
                    close=df.close,
                )
            ],
            layout={
                "height": 1000,
                "title": chart_name,
                "showlegend": True,
                "plot_bgcolor": colors["background"],
                "paper_bgcolor": colors["background"],
                "font": {"color": colors["text"]},
            },
        )
    elif chart_name == "EMA":
        df.index = df.date
        close_ema_10 = df.close.ewm(span=10).mean()
        close_ema_15 = df.close.ewm(span=15).mean()
        close_ema_30 = df.close.ewm(span=30).mean()
        close_ema_100 = df.close.ewm(span=100).mean()
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=list(close_ema_10.index), y=list(close_ema_10), name="10 Days"
                ),
                go.Scatter(
                    x=list(close_ema_15.index), y=list(close_ema_15), name="15 Days"
                ),
                go.Scatter(
                    x=list(close_ema_30.index), y=list(close_ema_30), name="30 Days"
                ),
                go.Scatter(
                    x=list(close_ema_100.index),
                    y=list(close_ema_100),
                    name="100 Days",
                ),
            ],
            layout={
                "height": 1000,
                "title": chart_name,
                "showlegend": True,
                "plot_bgcolor": colors["background"],
                "paper_bgcolor": colors["background"],
                "font": {"color": colors["text"]},
            },
        )
    elif chart_name == "MACD":
        df["MACD"], df["signal"], df["hist"] = (
            stock["macd"],
            stock["macds"],
            stock["macdh"],
        )
        fig = go.Figure(
            data=[
                go.Scatter(x=list(df.date), y=list(df.MACD), name="MACD"),
                go.Scatter(x=list(df.date), y=list(
                    df.signal), name="Signal"),
                go.Scatter(
                    x=list(df.date),
                    y=list(df["hist"]),
                    line=dict(color="royalblue", width=2, dash="dot"),
                    name="Hitogram",
                ),
            ],
            layout={
                "height": 1000,
                "title": chart_name,
                "showlegend": True,
                "plot_bgcolor": colors["background"],
                "paper_bgcolor": colors["background"],
                "font": {"color": colors["text"]},
            },
        )
    elif chart_name == "RSI":
        rsi_6 = stock["rsi_6"]
        rsi_12 = stock["rsi_12"]
        fig = go.Figure(
            data=[
                go.Scatter(x=list(df.date), y=list(
                    rsi_6), name="RSI 6 Day"),
                go.Scatter(x=list(df.date), y=list(
                    rsi_12), name="RSI 12 Day"),
            ],
            layout={
                "height": 1000,
                "title": chart_name,
                "showlegend": True,
                "plot_bgcolor": colors["background"],
                "paper_bgcolor": colors["background"],
                "font": {"color": colors["text"]},
            },
        )
    else:
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=list(df['date']), y=list(df['close']), fill="tozeroy", name="close"
                )
            ],
            layout={
                "height": 1000,
                "title": chart_name,
                "showlegend": True,
                "plot_bgcolor": colors["background"],
                "paper_bgcolor": colors["background"],
                "font": {"color": colors["text"]},
            },
        )

    return add_range_bar(fig)


def add_range_bar(figure):
    figure.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            activecolor=colors["line"],
            bgcolor=colors["background"],
            buttons=list(
                [
                    dict(count=7, label="10D",
                         step="day", stepmode="backward"),
                    dict(
                        count=15, label="15D", step="day", stepmode="backward"
                    ),
                    dict(
                        count=1, label="1m", step="month", stepmode="backward"
                    ),
                    dict(
                        count=3, label="3m", step="month", stepmode="backward"
                    ),
                    dict(
                        count=6, label="6m", step="month", stepmode="backward"
                    ),
                    dict(count=1, label="1y", step="year",
                         stepmode="backward"),
                    dict(count=5, label="5y", step="year",
                         stepmode="backward"),
                    dict(count=1, label="YTD",
                         step="year", stepmode="todate"),
                    dict(step="all"),
                ]
            ),
        ),
    )
    return figure


