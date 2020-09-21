import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from page_navigation.navbar import navbar
from page_navigation.sidebar import sidebar
from pages import trade_journal
from pages.analysis import overview, exit_quality, reward_risk, win_loss

pages = [overview, win_loss, reward_risk, exit_quality, trade_journal]
analysis_pages = [overview, win_loss, reward_risk, exit_quality]

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "12rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

content = html.Div(id="page-content", style=CONTENT_STYLE)
centrally_stored_data = dcc.Store(id='store-trade-data', storage_type='local')


app.layout = html.Div([dcc.Location(id="url"), navbar.layout, sidebar.layout, content, centrally_stored_data])


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

#Test for sending data to any page
@app.callback(
    Output('win-rate','children'),
    [Input('store-trade-data', 'modified_timestamp')],
    [State('store-trade-data', 'data')]
)
def update_win_rate(storage_timestamp, stored_data):
    return len(stored_data)


if __name__ == "__main__":
    app.run_server(port=8888, debug=True)
