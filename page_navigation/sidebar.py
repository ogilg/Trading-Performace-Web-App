import dash_bootstrap_components as dbc
import dash_html_components as html

from pages import overview, win_loss, reward_risk, exit_quality, upload_trades

pages = [overview, win_loss, reward_risk, exit_quality, upload_trades]

page_links = []
for page_name in pages:
    page_links.append(
        dbc.NavLink(page_name.page.name, href=page_name.page.path, id=page_name.page.id, style={'color': 'white'}))
    page_links.append(html.Br())

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 59,
    "left": 0,
    "bottom": 0,
    "width": "13rem",
    "padding": "1rem 1rem",
    "background-color": "#1218de",
}

sidebar = html.Div(
    [
        html.H5("Trade Performance Analysis", className="display-5", style={'color': 'white'}),
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
