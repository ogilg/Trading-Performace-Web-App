import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
from pages import overview, win_loss, reward_risk, exit_quality, upload_trades
from navbar import navbar

pages = [overview, win_loss, reward_risk, exit_quality, upload_trades]

page_links = []
for page_name in pages:
    page_links.append(dbc.NavLink(page_name.page.name, href=page_name.page.path, id=page_name.page.id))
    page_links.append(html.Br())

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 55,
    "left": 0,
    "bottom": 0,
    "width": "13rem",
    "padding": "1rem 1rem",
    "background-color": "#1218de",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "15rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H5("Trade Performance Analysis", className="display-5", style={'color':'white'}),
        html.Hr(),

        dbc.Nav(
            page_links,
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
    className="pretty_container",
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), navbar, sidebar, content])




# @app.callback(
#     Output('overview', 'active'),
#     [Input('url', 'pathname')])
# def toggle_active_links(pathname):
#     print("toggle", pathname)
#     return map(lambda path : path == pathname, pages)

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return html.P("Choose a page")
    for page_name in pages:
        if page_name.page.path == pathname:
            return page_name.page.layout
    return '404'

# if __name__ == '__main__':
#     app.run_server(debug=True)
if __name__ == "__main__":
    app.run_server(port=8888)