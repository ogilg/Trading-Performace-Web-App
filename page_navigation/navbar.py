import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from PIL import Image
from app import app

GAMMA_IMAGE = Image.open(r'C:\Users\oscar\PycharmProjects\Trading-Performace-Web-App\images\gamma.png')
from pages import overview, win_loss, reward_risk, exit_quality, upload_trades


search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button("Search", color="primary", className="ml-2"),
            width="auto",
        ),
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.A(html.Img(src=GAMMA_IMAGE, height="40px"),href="https://icons8.com",)),
                    dbc.Col(
                        dbc.NavItem(dbc.NavLink("Analysis", active = True, href=overview.page.path))
                    ),
                ],
                align="center",
                no_gutters=True,
            ),
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
    ],
    color="dark",
    dark=True,
    style={
        'top': 0,
        'left':0,
        "position": "fixed",
        'width' : '100%',
        'height': '8%',
    },
)

