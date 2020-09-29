from datetime import datetime, timedelta

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from pages.page import Page

sample_data = px.data.stocks()
sample_data = pd.DataFrame(sample_data)

page = Page("Diversification")
page.set_path('/analysis/diversification')
metrics = ['asset-list']
page.set_storage(metrics)

page.set_layout([
    html.Div([]),
])

# app.callback(
#     [], # output
#     [Input(page.id + '-asset-list', 'modified_timestamp')],
#     [State(page.id+'-asset-list', 'data')]]
# )
# def update_asset_allocation_figures(asset_list):
#     pass
