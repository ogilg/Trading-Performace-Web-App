import dash_html_components as html
from pages.analysis.asset_mode_dropdown import generate_analysis_mode_dropdown
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
from app import app

from pages.page import Page

page = Page('Overview')
page.set_path('/analysis/overview')

asset_list = ['ALL ASSETS', 'GOOG', 'AMZN']
asset_dropdown = generate_analysis_mode_dropdown(asset_list)
overview_metrics = ['p&l', 'rate-of-return']

page.set_storage(overview_metrics)

metrics = html.Div(
            [html.H3(id="p&l"), html.P("P&L")],
            id="p&l",
            className="mini_container",
        )


page.set_layout(html.Div([
    html.H1(
        page.name,
        style={"margin-bottom": "10px",
               "margin-left": "4px",
               },
    ),

    html.Div(children='''
            Trading activity overview.
        '''),
    asset_dropdown,
    metrics,
]))


@app.callback(
    Output("p&l", "children"),
    [Input('overview-p&l', 'modified_timestamp')],
    [State('overview-p&l', 'data')]
)
def update_profit(ts, profit):
    return profit or 'Confirm data'
