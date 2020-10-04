import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from model.diversification_data_processor import DiversificationDataProcessor
from pages.page import Page

sample_data = px.data.stocks()
sample_data = pd.DataFrame(sample_data)

page = Page("Diversification")
page.set_path('/analysis/diversification')
metrics = ['asset-list', 'number-of-shares']
page.set_storage(metrics)

page.set_layout([
    html.H1(
        page.name,
        style={"margin-bottom": "10px",
               "margin-left": "4px",
               },
    ),
    html.Br(),
    dcc.Graph(id='sunburst'),
    dcc.Graph(id='industry-pie-chart'),
    dcc.Graph(id='sector-pie-chart'),
    dcc.Graph(id='diversification-map'),
])


# TODO: speed up with caching and prevent initial call
@app.callback(
    [Output('diversification-map', 'figure'), Output('industry-pie-chart', 'figure'), Output('sector-pie-chart', 'figure'), Output('sunburst', 'figure')],
    [Input('store-central-data', 'modified_timestamp')],
    [State(page.id + '-asset-list', 'data'), State(page.id + '-number-of-shares', 'data')],
)
def update_asset_allocation_figures(timestamp, asset_list, number_of_shares):
    if timestamp is None:
        raise PreventUpdate
    diversification_data_processor = DiversificationDataProcessor(asset_list, number_of_shares)
    map_figure = diversification_data_processor.create_country_map_figure()
    industry_data_figure = diversification_data_processor.create_industry_figure()
    sector_figure = diversification_data_processor.create_sector_figure()
    sunburst_figure = diversification_data_processor.create_sunburst()

    return map_figure, industry_data_figure, sector_figure, sunburst_figure
