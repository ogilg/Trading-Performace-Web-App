import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
from pages import overview, win_loss, reward_risk, exit_quality
from navbar import navbar


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 55,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "1rem 1rem",
    "background-color": "#1218de",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H4("Trade Performance Analysis", className="display-4", style={'color':'white'}),
        html.Hr(),

        dbc.Nav(
            [
                dbc.NavLink(overview.page.name, href=overview.page.path, id=overview.page.id),
                html.Br(),
                dbc.NavLink(win_loss.page.name, href=win_loss.page.path, id=win_loss.page.id),
                html.Br(),
                dbc.NavLink(reward_risk.page.name, href=reward_risk.page.path, id=reward_risk.page.id),
                html.Br(),
                dbc.NavLink(exit_quality.page.name, href=exit_quality.page.path, id=exit_quality.page.id),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), navbar, sidebar, content])

pages = ['/','/pages/overview', '/pages/page-2']


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
    elif pathname == overview.page.path:
        return overview.page.layout
    elif pathname == win_loss.page.path:
        return win_loss.page.layout
    elif pathname == reward_risk.page.path:
        return reward_risk.page.layout
    elif pathname == exit_quality.page.path:
        return exit_quality.page.layout
    else:
        return '404'

# if __name__ == '__main__':
#     app.run_server(debug=True)
if __name__ == "__main__":
    app.run_server(port=8888)