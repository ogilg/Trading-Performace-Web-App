import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from pages.page import Page
from pages.analysis.asset_mode_dropdown import generate_analysis_mode_dropdown

sample_data = px.data.stocks()
sample_data = pd.DataFrame(sample_data)

fig = px.line(sample_data, x='date', y='GOOG')

page = Page("Win-Loss")
page.set_path('/analysis/win-loss')
metrics = ['profit-list']
page.set_storage(metrics)

asset_list = ['ALL ASSETS', 'GOOG', 'AMZN']
asset_dropdown = generate_analysis_mode_dropdown(asset_list)

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
            id='win-percentage',
            figure=fig
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
    wins = [profit > 0 for profit in profit_list]
    num_wins = wins.count(True)
    num_losses = len(profit_list) - num_wins
    win_rate = num_losses / len(profit_list)
    expectancy = sum(profit_list)/float(len(profit_list))
    return "{:.2%}".format(win_rate), round(expectancy, 2), len(profit_list)



