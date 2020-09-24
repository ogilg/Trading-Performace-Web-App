import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime, timedelta
import yfinance as yf
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from app import app

from pages.page import Page

page = Page('Benchmark-Comparison')
page.set_path('/analysis/benchmark-comparison')

page.set_storage(['asset-list'])

page.set_layout([
    html.H1(
        page.name,
        style={"margin-bottom": "10px",
               "margin-left": "4px",
               },
    ),
    dcc.DatePickerRange(
        id='date-picker-range',  # ID to be used for callback
        # min_date_allowed = calendar_start_date,
        max_date_allowed=datetime.today(),  # maximum date allowed on the DatePickerRange component
        initial_visible_month=datetime.today(),  # the month initially presented when the user opens the calendar
        start_date=(datetime.today() - timedelta(30)).date(),
        end_date=datetime.today().date(),
        display_format='MMM Do, YY',
        persistence=True,
        persisted_props=['start_date'],
        updatemode='bothdates',

    ),
    dcc.Graph(id='benchmark-comparison-graph')
])


@app.callback(
    Output('benchmark-comparison-graph', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('benchmark-comparison-asset-list', 'modified_timestamp')],
    [State('benchmark-comparison-asset-list', 'data')]
)
def update_output(start_date, end_date, ts, asset_list):
    stock_code = asset_list[0]

    stock_ticker = yf.Ticker(stock_code)
    stock_info = stock_ticker.info

    df_stock = yf.download(tickers=stock_code, start=start_date, end=end_date, auto_adjust=False)
    df_index = yf.download(tickers='^GSPC', start=start_date, end=end_date, auto_adjust=False)
    df_stock = df_stock.reset_index()
    df_index = df_index.reset_index()
    for key in ['Open', 'High', 'Close', 'Low']:
        df_stock[key] = df_stock[key].astype('float64')
    for key in ['Open', 'High', 'Close', 'Low']:
        df_index[key] = df_index[key].astype('float64')

    benchmark_figure = go.Figure()
    benchmark_figure.add_trace(go.Scatter(
        x=df_stock['Date'],
        y=((df_stock['Close'] - df_stock['Close'][0]) / df_stock['Close'][0]) * 100,
        name=f"{stock_code.upper()} growth"
    ))

    benchmark_figure.add_trace(go.Scatter(
        x=df_index['Date'],
        y=((df_index['Close'] - df_index['Close'][0]) / df_index['Close'][0]) * 100,
        name="S&P500 growth"
    ))

    benchmark_figure.add_trace(go.Scatter(
        x=df_stock['Date'],
        y=((df_stock['Close'] - df_stock['Close'][0]) / df_stock['Close'][0]) * 100 - (
                (df_index['Close'] - df_index['Close'][0]) / df_index['Close'][0]) * 100,
        name="Comparison"
    ))

    stock_name = stock_info['shortName']
    benchmark_figure.update_layout(
        xaxis_rangeslider_visible=False,
        title={
            'text': f'{stock_name.upper()} relative comparison with the S&P500',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        yaxis_title="Growth in %",
        font=dict(
            family="arial",
            color="black"
        ),
    )
    return benchmark_figure
