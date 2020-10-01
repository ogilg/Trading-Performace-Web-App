import dash_html_components as html
import numpy as np
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from helper_functions.get_t_bill_return import get_t_bill_return
from model.return_metrics import calculate_rate_of_return
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
    html.Div(
        [html.H3(id="sharpe-ratio"), html.P("Sharpe Ratio")],
        id="sharpe-ratio",
        className="mini_container",
    ),
])


def compute_total_amounts_traded(buy_prices, sell_prices, number_of_shares):
    total_buy_amount = 0
    total_sell_amount = 0
    for trade_id in range(len(buy_prices)):
        total_buy_amount += buy_prices[trade_id] * number_of_shares[trade_id]
        total_sell_amount += sell_prices[trade_id] * number_of_shares[trade_id]
    return total_buy_amount, total_sell_amount


@app.callback(
    [Output()],  # add output
    [Input('-'.join((page.id, 'entry-dates')), 'modified_timestamp')],
    [State('-'.join((page.id, 'asset-list')), 'data'), State('-'.join((page.id, 'buy-price-list')), 'data'),
     State('-'.join((page.id, 'sell-price-list')), 'data'), State('-'.join((page.id, 'number-of-shares')), 'data')]
)
def update_risk_metrics(timestamp, asset_list, buy_price_list, sell_price_list, number_of_shares):
    total_buy, total_sell = compute_total_amounts_traded(buy_price_list, sell_price_list, number_of_shares)
    rate_of_return = calculate_rate_of_return(total_buy, total_sell)
    t_bill_return = get_t_bill_return() # add start and end date
    std_excess_return = np.std(rate_of_return - t_bill_return)


    for example
        raise PreventUpdate
    return


@app.callback(
    Output('-'.join((page.id, 'asset-dropdown')), 'options'),
    [Input('-'.join((page.id, 'asset-list')), 'modified_timestamp')],
    [State('-'.join((page.id, 'asset-list')), 'data')]
)
def update_asset_dropdown(ts, asset_list):
    asset_options = [{'label': asset_name, 'value': asset_name} for asset_name in asset_list]
    return asset_options
