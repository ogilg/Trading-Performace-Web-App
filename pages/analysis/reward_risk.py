import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from pages.analysis.asset_mode_dropdown import generate_analysis_mode_dropdown
from pages.page import Page

page = Page("Reward-Risk")
page.set_path('/pages/reward_risk')
page.set_storage(['asset-list', 'buy-price-dict', 'sell-price-dict', 'number-of-shares'])

page.set_layout([
    html.H1(
        page.name,
        style={"margin-bottom": "10px",
               "margin-left": "4px",
               },
    ),

    generate_analysis_mode_dropdown(page.id),
    html.Div(id=page.id + '-content'),
])


# @app.callback(
#     [Output()], # add output
#     [Input('-'.join((page.id, 'entry-dates')), 'modified_timestamp')],
#     [State('-'.join((page.id, 'asset-list')), 'data'), State('-'.join((page.id, 'buy-price-dict')), 'data'),State('-'.join((page.id, 'sell-price-dict')), 'data'),State('-'.join((page.id, 'number-of-shares')), 'data')]
# )
# def update_risk_metrics(timestamp, asset_list, buy_price_dict, sell_price_dict, number_of_shares):
#     #TODO: add risk adjusted ratio figures
#     buy_price = buy_price_dict['AAPL'] for example
#     raise PreventUpdate
#     return

@app.callback(
    Output('-'.join((page.id, 'asset-dropdown')), 'options'),
    [Input('-'.join((page.id, 'asset-list')), 'modified_timestamp')],
    [State('-'.join((page.id, 'asset-list')), 'data')]
)
def update_asset_dropdown(ts, asset_list):
    asset_options = [{'label': asset_name, 'value': asset_name} for asset_name in asset_list]
    return asset_options