from datetime import date, timedelta

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pycountry
import yfinance as yf
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
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
    dcc.Graph(id='diversification-map')
])


def get_latest_price(stock_code):
    last_day = yf.download(tickers=stock_code, start='2020-03-03', end='2020-03-04', auto_adjust=False)
    return last_day['Close'][-1]


def get_stock_country(stock_code):
    print(stock_code)
    try:
        country_name = yf.Ticker(stock_code).info['country']
    except IndexError:
        return None, None
    except KeyError:
        return None, None
    country_code = pycountry.countries.get(name=country_name).alpha_3
    return country_code


# TODO: speed up with caching
@app.callback(
    Output('diversification-map', 'figure'),
    [Input(page.id + '-asset-list', 'modified_timestamp')],
    [State(page.id + '-asset-list', 'data'), State(page.id + '-number-of-shares', 'data')]
)
def update_asset_allocation_figures(timestamp, asset_list, number_of_shares):
    if timestamp is None:
        raise PreventUpdate
    print('Updating asset allocation figure')
    traded_amounts = []
    country_codes = []
    for trade_id in range(len(asset_list)):
        country_code = get_stock_country(asset_list[trade_id])
        country_codes.append(country_code)
        traded_amounts.append(get_latest_price(asset_list[trade_id]) * number_of_shares[trade_id])
    total_amount_traded = sum(traded_amounts)

    country_codes_filtered = []
    relative_amounts = []
    for trade_id in range(len(asset_list)):
        if country_codes[trade_id] is not None:
            country_codes_filtered.append(country_codes[trade_id])
            relative_amounts.append(round((traded_amounts[trade_id] / total_amount_traded) * 100, 2))

    data = pd.DataFrame(
        {'ISO code': country_codes, 'Relative investment amount': relative_amounts})
    grouped_data = data.groupby('ISO code')['Relative investment amount'].sum()
    final_relative_amounts = [grouped_data[country_code] for country_code in country_codes]

    map_data = pd.DataFrame({'ISO code': country_codes, 'Relative investment amount': final_relative_amounts})

    map_figure = go.Figure(data=go.Choropleth(
        locations=map_data['ISO code'],
        z=map_data['Relative investment amount'],
        # hovertext= df['text'],
        colorscale='Oryel',
        autocolorscale=False,
        colorbar_title='Relative investment amount (%)',
    ))

    map_figure.update_layout(

        title_text='Asset allocation per country'
    )

    return map_figure
