import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from page_navigation.navbar import navbar
from page_navigation.sidebar import sidebar
from model.trade import Trade
from model.portfolio import Portfolio
from pages import trade_journal
from pages.analysis import overview, exit_quality, reward_risk, win_loss, benchmark_comparison, create_storage

pages = [overview, win_loss, benchmark_comparison, reward_risk, exit_quality, trade_journal]
analysis_pages = [overview, win_loss, benchmark_comparison, reward_risk, exit_quality]
analysis_pages_building = [overview, win_loss, benchmark_comparison]

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "12rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

content = html.Div(id="page-content", style=CONTENT_STYLE)
centrally_stored_data = dcc.Store(id='store-central-data', storage_type='local')

app.layout = html.Div(
    [dcc.Location(id="url"), navbar.layout, sidebar.layout, content, centrally_stored_data,
     create_storage.create_storage_div(analysis_pages)])


@app.callback(
    [Output(page_name.page.id, 'active') for page_name in analysis_pages],
    [Input('url', 'pathname')])
def toggle_active_links(pathname):
    return [pathname == page_name.page.path for page_name in analysis_pages]


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return html.P("Choose a page")
    for page_name in pages:
        if page_name.page.path == pathname:
            return page_name.page.layout
    return '404'


def parse_trade_data(trade_data_list):
    trades = []
    for trade_data in trade_data_list:
        trade = Trade(asset_name=trade_data['STOCK CODE'], entry_date=trade_data['BUY DATE'],
                      exit_date=trade_data['SELL DATE'], buy_price=trade_data['BUY PRICE'],
                      number_of_shares=trade_data['NUMBER OF SHARES'])
        if trade.data_fetch_successful:
            trades.append(trade)

    portfolio = Portfolio(trades)
    return portfolio


# Test for sending data to any page
@app.callback(
    create_storage.create_output_list(analysis_pages_building),
    [Input('store-central-data', 'modified_timestamp')],
    [State('store-central-data', 'data')]
)
def broadcast_trade_data(storage_timestamp, stored_trade_data):
    print('Broadcasting Trade Data')
    if storage_timestamp is None:
        raise PreventUpdate
    portfolio = parse_trade_data(stored_trade_data)
    profit = portfolio.calculate_total_profit()
    profit_list = portfolio.profits
    rate_of_return = portfolio.find_rate_of_return()

    aggregate_profit_by_day = portfolio.calculate_aggregate_profit_by_day().reset_index()

    exit_dates = [trade.exit_date for trade in portfolio.trade_list]

    asset_list = portfolio.get_asset_list_from_trades()
    return [profit, rate_of_return, aggregate_profit_by_day.to_dict(), profit_list, exit_dates, asset_list]


if __name__ == "__main__":
    app.run_server(port=8888, debug=True)
