from datetime import datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from model.date_utils import date_range

from app import app
from pages.page import Page
from pages.analysis.asset_mode_dropdown import generate_analysis_mode_dropdown

sample_data = px.data.stocks()
sample_data = pd.DataFrame(sample_data)

fig = px.line(sample_data, x='date', y='GOOG')

page = Page("Win-Loss")
page.set_path('/analysis/win-loss')
metrics = ['profit-list', 'exit-dates']
page.set_storage(metrics)

asset_list = ['ALL ASSETS', 'GOOG', 'AMZN']
asset_dropdown = generate_analysis_mode_dropdown(page.id)

page.set_layout([
    html.H1(
        page.name,
        style={"margin-bottom": "10px",
               "margin-left": "4px",
               },
    ),
    asset_dropdown,
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
    ),
]
)


# Selectors -> well text
@app.callback(
    [Output("win-rate", "children"), Output("expectancy", "children"), Output('number-of-trades', 'children')],
    [Input('win-loss-profit-list', 'modified_timestamp')],
    [State('win-loss-profit-list', 'data')],
)
def update_well_text(ts, profit_list):
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
    [Input('win-loss-exit-dates', 'modified_timestamp')],
    [State('win-loss-exit-dates', 'data'), State('win-loss-profit-list', 'data')]
)
def update_win_rate_graph(ts, exit_dates, profit_list):
    exit_dates = [datetime.strptime(exit_date.split('T')[0], '%Y-%m-%d') for exit_date in exit_dates]
    dated_profits = sorted([(exit_date, profit > 0) for exit_date, profit in zip(exit_dates, profit_list)])
    first_exit_date, last_exit_date = dated_profits[0][0], dated_profits[-1][0]

    wins_to_date = 0
    win_rate_data = []
    num_trades = 0

    for date in date_range(first_exit_date, last_exit_date):
        if str(date) in str(dated_profits[num_trades][0]):
            wins_to_date += 1 if dated_profits[num_trades][1] else 0
            win_rate = wins_to_date / (num_trades + 1)
            num_trades += 1
        win_rate_data.append({'Date': date, 'Win Rate': win_rate})

    win_rate_dataframe = pd.DataFrame(win_rate_data)

    win_rate_figure = px.line(win_rate_dataframe, x='Date', y='Win Rate', title='Win rate through time')
    win_rate_figure.update_yaxes(range=[-0.01, 1.01])
    return win_rate_figure
