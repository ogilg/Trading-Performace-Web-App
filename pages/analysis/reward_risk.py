import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from helper_functions.date_utils import remove_day_time
from helper_functions.get_t_bill_return import get_t_bill_return
from helper_functions.ratio_metrics import *
from helper_functions.return_metrics import calculate_rate_of_return, calculate_gain_to_pain
from pages.page import Page

page = Page("Reward-Risk")
page.set_path('/pages/reward_risk')
page.set_storage(['asset-list', 'aggregate-value-by-day', 'portfolio-gains', 'portfolio-losses'])

default_gauge = {'axis': {'range': [-1, 4]},
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
    gauge=default_gauge))

sortino_ratio_fig = go.Figure()
sortino_ratio_fig.add_trace(go.Indicator(
    domain={'x': [0, 1], 'y': [0, 1]},
    value=0,
    mode="gauge+number+delta",
    title={'text': "Sortino ratio"},
    gauge=default_gauge))

gain_to_pain_ratio_fig = go.Figure()
gain_to_pain_ratio_fig.add_trace(go.Indicator(
    domain={'x': [0, 1], 'y': [0, 1]},
    value=0,
    mode="gauge+number+delta",
    title={'text': "Gain to Pain ratio"},
    gauge=default_gauge))

page.set_layout([
    html.H1(
        'Risk Adjusted Return',
        style={"margin-bottom": "10px",
               "margin-left": "4px",
               },
    ),
    html.Div(children='''
            Risk-adjusted metrics calculated on portfolio.
        '''),
    html.Br(),
    dcc.Graph(id='sharpe_ratio_indicator', figure=sharpe_ratio_fig),
    html.Br(),
    dcc.Graph(id='sortino_ratio_indicator', figure=sortino_ratio_fig),
    html.Br(),
    dcc.Graph(id='gain_to_pain_ratio_indicator', figure=gain_to_pain_ratio_fig),
])


@app.callback(
    [Output('sharpe_ratio_indicator', 'figure'),
     Output('sortino_ratio_indicator', 'figure'),
     Output('gain_to_pain_ratio_indicator', 'figure')],
    [Input('-'.join((page.id, 'aggregate-value-by-day')), 'modified_timestamp')],
    [State('-'.join((page.id, 'aggregate-value-by-day')), 'data'),
     State('-'.join((page.id, 'portfolio-gains')), 'data'),
     State('-'.join((page.id, 'portfolio-losses')), 'data'), ]
)
def update_risk_metrics(timestamp, aggregate_value_by_day, portfolio_gains, portfolio_losses):
    if aggregate_value_by_day is None:
        raise PreventUpdate

    start_date = remove_day_time(aggregate_value_by_day['Date'][0])
    end_date = remove_day_time(aggregate_value_by_day['Date'][-1])
    t_bill_return = get_t_bill_return(start_date, end_date)  # add start and end date
    return_std = np.std(aggregate_value_by_day['Stock Close'])
    portfolio_return = calculate_rate_of_return(aggregate_value_by_day['Stock Close'][0],
                                                aggregate_value_by_day['Stock Close'][-1]) * 100
    negative_return_std = calculate_negative_return_std(aggregate_value_by_day)

    sharpe_ratio = calculate_sharpe_ratio(portfolio_return, t_bill_return, return_std)
    sortino_ratio = calculate_sortino_ratio(portfolio_return, t_bill_return, negative_return_std)

    try :
        gain_to_pain_ratio = calculate_gain_to_pain(portfolio_gains, portfolio_losses)
    except ZeroDivisionError:
        gain_to_pain_ratio = 100

    sharpe_ratio_fig = go.Figure()
    sharpe_ratio_fig.add_trace(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=sharpe_ratio,
        mode="gauge+number+delta",
        title={'text': "Sharpe ratio"},
        gauge=default_gauge))

    sortino_ratio_fig = go.Figure()
    sortino_ratio_fig.add_trace(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=sortino_ratio,
        mode="gauge+number+delta",
        title={'text': "Sortino ratio"},
        gauge=default_gauge))

    gain_to_pain_ratio_fig = go.Figure()
    gain_to_pain_ratio_fig.add_trace(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=gain_to_pain_ratio,
        mode="gauge+number+delta",
        title={'text': "Gain to Pain ratio"},
        gauge=default_gauge))

    return sharpe_ratio_fig, sortino_ratio_fig, gain_to_pain_ratio_fig


def calculate_negative_return_std(aggregate_value_by_day):
    prev_day = 0
    negative_returns = []
    for day_value in aggregate_value_by_day['Stock Close']:
        if day_value < prev_day:
            negative_returns.append(day_value)

        prev_day = day_value

    return np.std(negative_returns)
