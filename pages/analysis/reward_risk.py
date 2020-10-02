import dash_html_components as html
import numpy as np
import yfinance as yf
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import

from app import app
from helper_functions.get_t_bill_return import get_t_bill_price
from model.return_metrics import calculate_rate_of_return
from pages.analysis.asset_mode_dropdown import generate_analysis_mode_dropdown
from pages.page import Page

page = Page("Reward-Risk")
page.set_path('/pages/reward_risk')
page.set_storage(['asset-list', 'aggregate-profit-by-day'])

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
    Output('sharpe-ratio', 'children'),  # add output
    [Input('-'.join((page.id, 'entry-dates')), 'modified_timestamp')],
    [State('-'.join((page.id, 'asset-list')), 'data'), State('-'.join((page.id, 'aggregate-profit-by-day')), 'data')]
)
def update_risk_metrics(timestamp, asset_list, aggregate_profit_by_day):
    start_date = aggregate_profit_by_day['Date'][0]
    end_date = aggregate_profit_by_day['Date'][-1]
    t_bill_price = get_t_bill_price() # add start and end date
    std_excess_return = np.std(aggregate_profit_by_day['Profit Open'] - t_bill_price)


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
