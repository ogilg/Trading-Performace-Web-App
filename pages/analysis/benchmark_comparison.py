from datetime import datetime, timedelta

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import yfinance as yf
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from pages.analysis.asset_mode_dropdown import generate_analysis_mode_dropdown

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
    html.Div(children='''
            Choose an asset to benchmark
        '''),
    html.Br(),
    generate_analysis_mode_dropdown(page.id),
    html.Br(),
    dcc.DatePickerRange(
        id='date-picker-range',
        # min_date_allowed = calendar_start_date,
        max_date_allowed=datetime.today(),  # maximum date allowed on the DatePickerRange component
        initial_visible_month=datetime.today(),  # the month initially presented when the user opens the calendar
        start_date=(datetime.today() - timedelta(30)).date(),
        end_date=datetime.today().date(),
        display_format='MMM Do, YY',
        persistence=True,
        persisted_props=['start_date'],
        updatemode='bothdates',
        className='date_picker',

    ),
    html.Br(),
    dcc.Graph(id='benchmark-comparison-graph')
])


@app.callback(
    Output('benchmark-comparison-asset-dropdown', 'options'),
    [Input('benchmark-comparison-asset-list', 'modified_timestamp')],
    [State('benchmark-comparison-asset-list', 'data')]
)
def update_asset_dropdown(ts, asset_list):
    asset_options = [{'label': asset_name, 'value': asset_name} for asset_name in asset_list]
    return asset_options


@app.callback(
    Output('benchmark-comparison-graph', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('benchmark-comparison-asset-dropdown', 'value')],
)
def update_output(start_date, end_date, stock_code):
    try:
        stock_ticker = yf.Ticker(stock_code)
    except AttributeError:
        raise PreventUpdate
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
        name=f"{stock_code.upper()}"
    ))

    benchmark_figure.add_trace(go.Scatter(
        x=df_index['Date'],
        y=((df_index['Close'] - df_index['Close'][0]) / df_index['Close'][0]) * 100,
        name="S&P500"
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
