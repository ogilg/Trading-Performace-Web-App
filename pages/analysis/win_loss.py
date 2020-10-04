from datetime import datetime, timedelta

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from helper_functions.date_utils import date_range
from pages.analysis.asset_mode_dropdown import generate_analysis_mode_dropdown
from pages.page import Page

sample_data = px.data.stocks()
sample_data = pd.DataFrame(sample_data)

page = Page("Win-Loss")
page.set_path('/analysis/win-loss')
metrics = ['profit-list', 'exit-dates', 'asset-list']
page.set_storage(metrics)

page.set_layout([
    html.H1(
        page.name,
        style={"margin-bottom": "10px",
               "margin-left": "4px",
               },
    ),
    generate_analysis_mode_dropdown(page.id),
    dbc.Row(
        [
            dbc.Col(html.Div(
                [html.H3(id="win-rate"), html.P("Win Rate")],
                id="win-rate",
                className="mini_container",
            ),
            ),
            dbc.Col(html.Div(
                [html.H3(id="number-of-trades"), html.P("Number Of Trades")],
                id="number-of-trades",
                className="mini_container",
            ),
            ),
            dbc.Col(html.Div(
                [html.H3(id="expectancy"), html.P("Expectancy")],
                id="expectancy",
                className="mini_container",
            ),
            ),
        ]
    ),

    dcc.Graph(
        id='win-rate-through-time',
    ), ]
)


@app.callback(
    [Output("win-rate", "children"), Output("expectancy", "children"), Output('number-of-trades', 'children')],
    [Input('win-loss-profit-list', 'modified_timestamp')],
    [State('win-loss-profit-list', 'data')],
)
def update_metrics(ts, profit_list):
    if profit_list is None or len(profit_list) == 0:
        raise PreventUpdate
    win_rate = calculate_win_rate(profit_list)
    expectancy = sum(profit_list) / float(len(profit_list))
    return "{:.2%}".format(win_rate), round(expectancy, 2), len(profit_list)


def calculate_win_rate(profit_list):
    wins = [profit > 0 for profit in profit_list]
    num_wins = wins.count(True)
    num_losses = len(profit_list) - num_wins
    win_rate = num_wins / len(profit_list)
    return win_rate


@app.callback(
    Output('win-rate-through-time', 'figure'),
    [Input('win-loss-exit-dates', 'modified_timestamp'), Input('win-loss-asset-dropdown', 'value')],
    [State('win-loss-exit-dates', 'data'), State('win-loss-profit-list', 'data'), State('win-loss-asset-list', 'data')]
)
def update_win_rate_graph(ts, selected_stock_code, unfiltered_exit_dates, unfiltered_profit_list, stock_codes):
    if unfiltered_exit_dates is None:
        raise PreventUpdate
    if selected_stock_code is not None:
        exit_dates, profit_list = filter_data_by_asset(selected_stock_code, stock_codes, unfiltered_exit_dates,
                                                       unfiltered_profit_list)
    else:
        exit_dates = unfiltered_exit_dates
        profit_list = unfiltered_profit_list

    exit_dates = [datetime.strptime(exit_date.split('T')[0], '%Y-%m-%d') for exit_date in exit_dates]
    dated_trades = construct_dated_trade_list(exit_dates, profit_list)
    first_exit_date, last_exit_date = dated_trades[0][0], dated_trades[-1][0]

    wins_to_date = num_trades = 0
    win_rate_data = []
    for date in date_range(first_exit_date, last_exit_date + timedelta(2)):
        if num_trades < len(profit_list) and str(date) in str(dated_trades[num_trades][0]):
            wins_to_date += 1 if dated_trades[num_trades][1] else 0
            win_rate = wins_to_date / (num_trades + 1)
            num_trades += 1
        win_rate_data.append({'Date': date, 'Win Rate': win_rate})

    win_rate_dataframe = pd.DataFrame(win_rate_data)
    win_rate_figure = px.line(win_rate_dataframe, x='Date', y='Win Rate', title='Win rate through time')
    win_rate_figure.update_yaxes(range=[-0.01, 1.01])
    return win_rate_figure


def construct_dated_trade_list(exit_dates, profit_list):
    return sorted([(exit_date, profit > 0) for exit_date, profit in zip(exit_dates, profit_list)])


def filter_data_by_asset(selected_stock_code, stock_codes, unfiltered_exit_dates, unfiltered_profit_list):
    exit_dates = profit_list = []
    for stock_id, code in enumerate(stock_codes):
        if code == selected_stock_code:
            exit_dates.append(unfiltered_exit_dates[stock_id])
            profit_list.append(unfiltered_profit_list[stock_id])

    return exit_dates, profit_list


@app.callback(
    Output('win-loss-asset-dropdown', 'options'),
    [Input('win-loss-asset-list', 'modified_timestamp')],
    [State('win-loss-asset-list', 'data')]
)
def update_asset_dropdown(ts, asset_list):
    if asset_list is None:
        raise PreventUpdate
    asset_options = [{'label': asset_name, 'value': asset_name} for asset_name in asset_list]
    return asset_options
