import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import dash_core_components as dcc

from app import app
from helper_functions.get_t_bill_return import get_t_bill_return
from model.date_utils import remove_day_time
from model.ratio_metrics import *
from model.return_metrics import calculate_rate_of_return, calculate_gain_to_pain
from pages.analysis.asset_mode_dropdown import generate_analysis_mode_dropdown
from pages.page import Page

page = Page("Reward-Risk")
page.set_path('/pages/reward_risk')
page.set_storage(['asset-list', 'aggregate-profit-by-day', 'portfolio-gains', 'portfolio-losses'])

sharpe_ratio_gauge = {'axis': {'range': [-1, 4]},
                      'bar': {'color': 'black'},
                      'steps': [
                          {'range': [-1, 1], 'color': 'red'},
                          {'range': [1, 2], 'color': 'orange'},
                          {'range': [2, 3], 'color': 'green'},
                          {'range': [3, 4], 'color': 'darkgreen'}],
                      }

sharpe_ratio_fig = go.Figure()
sharpe_ratio_fig.add_trace(go.Indicator(
    domain={'x': [0, 1], 'y': [0, 1]},
    value=0,
    mode="gauge+number+delta",
    title={'text': "Sharpe ratio"},
    gauge=sharpe_ratio_gauge))

sortino_ratio_gauge = {'axis': {'range': [-1, 4]},
                      'bar': {'color': 'black'},
                      'steps': [
                          {'range': [-1, 1], 'color': 'red'},
                          {'range': [1, 2], 'color': 'orange'},
                          {'range': [2, 3], 'color': 'green'},
                          {'range': [3, 4], 'color': 'darkgreen'}],
                      }

sortino_ratio_fig = go.Figure()
sortino_ratio_fig.add_trace(go.Indicator(
    domain={'x': [0, 1], 'y': [0, 1]},
    value=0,
    mode="gauge+number+delta",
    title={'text': "Sortino ratio"},
    gauge=sortino_ratio_gauge))


gain_to_pain_ratio_gauge = {'axis': {'range': [-1, 4]},
                      'bar': {'color': 'black'},
                      'steps': [
                          {'range': [-1, 1], 'color': 'red'},
                          {'range': [1, 2], 'color': 'orange'},
                          {'range': [2, 3], 'color': 'green'},
                          {'range': [3, 4], 'color': 'darkgreen'}],
                      }

gain_to_pain_ratio_fig = go.Figure()
gain_to_pain_ratio_fig.add_trace(go.Indicator(
    domain={'x': [0, 1], 'y': [0, 1]},
    value=0,
    mode="gauge+number+delta",
    title={'text': "Gain to Pain ratio"},
    gauge=gain_to_pain_ratio_gauge))


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
    html.Br(),
    dcc.Graph(id='sharpe_ratio_indicator', figure =sharpe_ratio_fig),
    html.Br(),
    dcc.Graph(id='sortino_ratio_indicator', figure =sortino_ratio_fig),
    html.Br(),
    dcc.Graph(id='gain_to_pain_ratio_indicator', figure =gain_to_pain_ratio_fig),
])


def compute_total_amounts_traded(buy_prices, sell_prices, number_of_shares):
    total_buy_amount = 0
    total_sell_amount = 0
    for trade_id in range(len(buy_prices)):
        total_buy_amount += buy_prices[trade_id] * number_of_shares[trade_id]
        total_sell_amount += sell_prices[trade_id] * number_of_shares[trade_id]
    return total_buy_amount, total_sell_amount


@app.callback(
    [Output('sharpe_ratio_indicator', 'figure'),
    Output('sortino_ratio_indicator', 'figure'),
    Output('gain_to_pain_ratio_indicator','figure')],
    [Input('-'.join((page.id, 'aggregate-profit-by-day')), 'modified_timestamp')],
    [State('-'.join((page.id, 'aggregate-profit-by-day')), 'data'),
     State('-'.join((page.id, 'portfolio-gains')), 'data'),
     State('-'.join((page.id, 'portfolio-losses')), 'data'),]
)
def update_risk_metrics(timestamp, aggregate_profit_by_day, portfolio_gains, portfolio_losses):
    start_date = remove_day_time(aggregate_profit_by_day['Date'][0])
    end_date = remove_day_time(aggregate_profit_by_day['Date'][-1])
    t_bill_return = get_t_bill_return(start_date, end_date)  # add start and end date
    return_std = np.std(aggregate_profit_by_day['Stock Close'])
    portfolio_return = calculate_rate_of_return(aggregate_profit_by_day['Stock Close'][0],
                                                aggregate_profit_by_day['Stock Close'][-1]) * 100
    neg_returns_list = [num for num in aggregate_profit_by_day['Stock Close'] if num < 0]
    std_downside_return = np.std(neg_returns_list)


    sharpe_ratio = calculate_sharpe_ratio(portfolio_return, t_bill_return, return_std)
    sortino_ratio = calculate_sortino_ratio(portfolio_return, t_bill_return, negative_return_std)
    gain_to_pain_ratio = calculate_gain_to_pain(portfolio_gains, portfolio_losses)

    sharpe_ratio_fig = go.Figure()
    sharpe_ratio_fig.add_trace(go.Indicator(
    domain={'x': [0, 1], 'y': [0, 1]},
    value=sharpe_ratio,
    mode="gauge+number+delta",
    title={'text': "Sharpe ratio"},
    gauge=sharpe_ratio_gauge))
    
    sortino_ratio_fig = go.Figure()
    sortino_ratio_fig.add_trace(go.Indicator(
    domain={'x': [0, 1], 'y': [0, 1]},
    value=sortino_ratio,
    mode="gauge+number+delta",
    title={'text': "Sortino ratio"},
    gauge=sortino_ratio_gauge))
    
    gain_to_pain_ratio_fig = go.Figure()
    gain_to_pain_ratio_fig.add_trace(go.Indicator(
    domain={'x': [0, 1], 'y': [0, 1]},
    value=gain_to_pain_ratio,
    mode="gauge+number+delta",
    title={'text': "Gain to Pain ratio"},
    gauge=gain_to_pain_ratio_gauge))
    
    return sharpe_ratio_fig, sortino_ratio_fig, gain_to_pain_ratio_fig

@app.callback(
    Output('-'.join((page.id, 'asset-dropdown')), 'options'),
    [Input('-'.join((page.id, 'asset-list')), 'modified_timestamp')],
    [State('-'.join((page.id, 'asset-list')), 'data')]
)
def update_asset_dropdown(ts, asset_list):
    asset_options = [{'label': asset_name, 'value': asset_name} for asset_name in asset_list]
    return asset_options
