import dash_html_components as html
from pages.analysis.asset_mode_dropdown import generate_analysis_mode_dropdown
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
from app import app

from pages.page import Page

page = Page('Overview')
page.set_path('/analysis/overview')

asset_list = ['ALL ASSETS', 'GOOG', 'AMZN']
asset_dropdown = generate_analysis_mode_dropdown(asset_list)
overview_metrics = ['p&l', 'rate-of-return', 'aggregate-profit-by-day']

page.set_storage(overview_metrics)

metrics = html.Div([
    dbc.Row(
        [
            dbc.Col(html.Div(
                [html.H3(id="p&l"), html.P("P&L")],
                id="p&l",
                className="mini_container",
            )
            ),
            dbc.Col(html.Div(
                [html.H3(id='rate-of-return'), html.P("Rate of Return")],
                id="rate-of-return",
                className="mini_container",
            )
            ),
            dbc.Col(html.Div(
                [html.H3(id='profit-factor'), html.P("Profit Factor")],
                id='profit-factor',
                className="mini_container",
            )
            ),
        ]
    ),
    dcc.Graph(id='aggregate-daily-profit-open',),
    dcc.Graph(id='aggregate-daily-profit-close'),
    ]
)

page.set_layout([
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
])


@app.callback(
    Output("p&l", "children"),
    [Input('overview-p&l', 'modified_timestamp')],
    [State('overview-p&l', 'data')]
)
def update_profit(ts, profit):
    if profit is None:
        return 'Confirm Data'
    return round(profit, 2)


@app.callback(
    [Output('rate-of-return', 'children'), Output('profit-factor', 'children')],
    [Input('overview-rate-of-return', 'modified_timestamp')],
    [State('overview-rate-of-return', 'data')]
)
def update_profit(ts, rate_of_return):
    if rate_of_return is None:
        raise PreventUpdate
    rate_of_return = round(rate_of_return, 2)
    return rate_of_return, rate_of_return + 1


@app.callback(
    [Output("aggregate-daily-profit-open", "figure"), Output("aggregate-daily-profit-close", "figure")],
    [Input('overview-aggregate-profit-by-day', 'modified_timestamp')],
    [State('overview-aggregate-profit-by-day', 'data')]
)
def update_profit(ts, aggregate_daily_profit):
    if aggregate_daily_profit is None:
        raise PreventUpdate
    profit_at_open = px.line(aggregate_daily_profit, x='Date', y='Profit Open', title='Profit at Open',)
    profit_at_close = px.line(aggregate_daily_profit, x='Date', y='Profit Close',  title='Profit at Close', color_discrete_map={'Profir Close': 'red'})
    add_line_to_figure(profit_at_close)
    add_line_to_figure(profit_at_open)
    return profit_at_open, profit_at_close

# output argument
def add_line_to_figure(fig):
    fig.update_layout(shapes=[
        dict(
            type='line',
            yref='y', y0=0, y1=0,
            xref='paper', x0=0, x1=1
        )
    ])

