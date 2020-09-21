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

asset_list = ['ALL ASSETS', 'GOOG', 'AMZN']
sessions = ['session 1', 'session 2']
asset_dropdown = generate_analysis_mode_dropdown(asset_list, sessions)

page.set_layout_with_storage(html.Div(
    [
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
        html.Div(id='data-length')
    ]
))


# Selectors -> well text
@app.callback(
    Output("win-rate", "children"),
    [Input('url', 'pathname')],
)
def update_well_text(pathname):
    return 56


# Selectors -> well text
@app.callback(
    Output("expectancy", "children"),
    [Input('url', 'pathname')],
)
def update_well_text(pathname):
    return 567


@app.callback(
    Output('data-th', 'children'),
    [Input('win-loss-data', 'modified_timestamp')],
    [State('win-loss-data', 'data')]
)
def store_data_length(ts, data):
    if ts is None:
        raise PreventUpdate
    return len(data)
