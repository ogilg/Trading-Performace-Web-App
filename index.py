import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from page_navigation.navbar import navbar
from page_navigation.sidebar import sidebar
from pages import overview, win_loss, reward_risk, exit_quality, upload_trades

pages = [overview, win_loss, reward_risk, exit_quality, upload_trades]

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "12rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), navbar.layout, sidebar.layout, content])


@app.callback(
    [Output(page_name.page.id, 'active') for page_name in pages],
    [Input('url', 'pathname')])
def toggle_active_links(pathname):
    return [pathname == page_name.page.path for page_name in pages]

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return html.P("Choose a page")
    for page_name in pages:
        if page_name.page.path == pathname:
            return page_name.page.layout
    return '404'

if __name__ == "__main__":
    app.run_server(port=8888)