from datetime import datetime, timedelta

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import yfinance as yf
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from pages.analysis.asset_mode_dropdown import generate_analysis_mode_dropdown
from pages.page import Page

page = Page("Exit-Quality")
page.set_path('/pages/exit_quality')
page.set_storage(['asset-list'])

exit_quality_gauge = {'axis': {'range': [-100, 100]},
                      'bar': {'color': "black"},
                      'steps': [
                          {'range': [-100, 0], 'color': "red"},
                          {'range': [0, 50], 'color': "orange"},
                          {'range': [50, 75], 'color': 'green'},
                          {'range': [75, 100], 'color': 'darkgreen'}],
                      }

exit_quality_fig = go.Figure()
exit_quality_fig.add_trace(go.Indicator(
    domain={'x': [0, 1], 'y': [0, 1]},
    value=0,
    mode="gauge+number+delta",
    title={'text': "Exit quality"},
    gauge=exit_quality_gauge))

gauge_layout = html.Div([
    # maybe remove buttons since date picker makes them redundant
    html.Button('Within period', id='full-period', n_clicks=0),
    html.Br(),
    html.Button('Within 1 day of period', id='within-one-day', n_clicks=0, className='button'),
    html.Br(),
    html.Button('Within 1 week of period', id='within-one-week', n_clicks=0, className='button'),
    html.Br(),
    html.Button('Within 1 month of period', id='within-one-month', n_clicks=0, className='button'),

    html.Br(),
    html.Br(),

    dcc.DatePickerRange(
        id='my-date-picker-range',  # ID to be used for callback
        max_date_allowed=datetime.today(),  # maximum date allowed on the DatePickerRange component
        initial_visible_month=datetime.today(),  # the month initially presented when the user opens the calendar
        start_date=(datetime.today() - timedelta(30)).date(),
        end_date=datetime.today().date(),
        display_format='MMM Do, YY',
        persistence=True,
        persisted_props=['start_date'],
        updatemode='bothdates',

    ),
    dcc.Graph(id='exit-quality-indicator', figure=exit_quality_fig)

])

page.layout = [
    html.H1(
        page.name,
        style={"margin-bottom": "10px",
               "margin-left": "4px",
               },
    ),
    generate_analysis_mode_dropdown(page.id),
    gauge_layout
]


@app.callback(
    Output('exit-quality-indicator', 'figure'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date'),
     Input('full-period', 'n_clicks'),
     Input('within-one-day', 'n_clicks'),
     Input('within-one-week', 'n_clicks'),
     Input('within-one-month', 'n_clicks'),
     Input('exit-quality-asset-dropdown', 'value')]
)
def update_output(start_date, end_date, full_period, within_one_day, within_one_week, within_one_month, stock_code):
    if stock_code is None:
        raise PreventUpdate
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    start_date = datetime.strptime(start_date.split('T')[0], '%Y-%m-%d')
    end_date = datetime.strptime(end_date.split('T')[0], '%Y-%m-%d')
    if 'full-period' in changed_id:
        pass
    elif 'within-one-day' in changed_id:
        start_date = start_date - timedelta(1)
        end_date = end_date + timedelta(1)
    elif 'within-one-week' in changed_id:
        start_date = start_date - timedelta(7)
        end_date = end_date + timedelta(7)
    elif 'within-one-month' in changed_id:
        start_date = start_date - timedelta(30)
        end_date = end_date + timedelta(30)

    sell_price = 90
    buy_price = 100

    stock_data = yf.download(stock_code, start=start_date, end=end_date)

    sorted_stock_closes = sorted(stock_data['Close'], reverse=True)
    max_close = round(sorted_stock_closes[0], 2)

    actual_return = ((sell_price - buy_price) / buy_price) * 100
    max_return = ((max_close - buy_price) / buy_price) * 100

    exit_rating = (actual_return / max_return) * 100

    exit_quality_fig = go.Figure()
    exit_quality_fig.add_trace(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=exit_rating,
        mode="gauge+number+delta",
        title={'text': "Exit quality"},
        gauge=exit_quality_gauge
    ))
    return exit_quality_fig

@app.callback(
    Output('exit-quality-asset-dropdown', 'options'),
    [Input('exit-quality-asset-list', 'modified_timestamp')],
    [State('exit-quality-asset-list', 'data')]
)
def update_asset_dropdown(ts, asset_list):
    asset_options = [{'label': asset_name, 'value': asset_name} for asset_name in asset_list]
    return asset_options
