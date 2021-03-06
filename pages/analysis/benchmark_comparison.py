from datetime import datetime, timedelta

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import yfinance as yf
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from pages.analysis.asset_mode_dropdown import generate_analysis_mode_dropdown
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
    if asset_list is None:
        raise PreventUpdate
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
        stock_info = stock_ticker.info
    except AttributeError:
        raise PreventUpdate


    df_stock = yf.download(tickers=stock_code, start=start_date, end=end_date, auto_adjust=False).reset_index()
    stock_index_data = yf.download(tickers='^GSPC', start=start_date, end=end_date, auto_adjust=False).reset_index()

    stock_close_data = df_stock['Close'].astype('float64')
    stock_index_close_data = stock_index_data['Close'].astype('float64')

    benchmark_figure = go.Figure()
    benchmark_figure.add_trace(go.Scatter(
        x=df_stock['Date'],
        y=((stock_close_data - stock_close_data[0]) / stock_close_data[0]) * 100,
        name=f"{stock_code.upper()}"
    ))

    benchmark_figure.add_trace(go.Scatter(
        x=stock_index_data['Date'],
        y=((stock_index_close_data - stock_index_close_data[0]) / stock_index_close_data[0]) * 100,
        name="S&P500"
    ))

    benchmark_figure.add_trace(go.Scatter(
        x=df_stock['Date'],
        y=((df_stock['Close'] - df_stock['Close'][0]) / df_stock['Close'][0]) * 100 - (
                (stock_index_close_data - stock_index_close_data[0]) / stock_index_close_data[0]) * 100,
        name="Difference"
    ))

    stock_name = stock_info['shortName']
    benchmark_figure.update_layout(
        xaxis_rangeslider_visible=False,
        title={
            'text': f'{stock_name.upper()} vs S&P500',
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
