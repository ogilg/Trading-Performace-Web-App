import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from pages.page import Page
from app import app
page = Page("Win-Loss")
page.set_path('/pages/win-loss')

page.layout = html.Div(
    [
        html.H1(
            page.name,
            style={"margin-bottom": "10px"},
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(
                    [html.H6(id="win_rate"), html.P("Win Rate")],
                        id="win_rate",
                        className="mini_container",
                    ),
                ),
                dbc.Col(html.Div(
                        [html.H6(id="expectancy"), html.P("Expectancy")],
                        id="expectancy",
                        className="mini_container",
                    ),
                ),
                dbc.Col(html.Div(
                        [html.H6(id="oilText"), html.P("Oil")],
                        id="oil",
                        className="mini_container",
                    ),
                )
            ]
        )
    ]
)


# Selectors -> well text
@app.callback(
    Output("win_rate", "children"),
    [Input('url', 'pathname')],
)
def update_well_text(pathname):
    return 56

# Selectors -> well text
@app.callback(
    Output("expectancy", "children"),
    [Input('url', 'pathname')],
)
def update_well_text(pathname):
    return 567


