import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from dash.dependencies import Input, Output

from pages.page import Page
from app import app
import plotly.express as px
import numpy as np
import pandas as pd
sample_data = px.data.stocks()
sample_data = pd.DataFrame(sample_data)

fig = px.line(sample_data, x = 'date',y = 'GOOG')

page = Page("Win-Loss")
page.set_path('/pages/win-loss')

page.layout = html.Div(
    [
        html.H1(
            page.name,
            style={"margin-bottom": "10px",
                   "margin-left":"4px"
                   },
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(
                    [html.H3(id="win_rate"), html.P("Win Rate")],
                        id="win_rate",
                        className="mini_container",
                    ),
                ),
                dbc.Col(html.Div(
                        [html.H3(id="expectancy"), html.P("Expectancy")],
                        id="expectancy",
                        className="mini_container",
                    ),
                ),
            ]
        ),

        dcc.Graph(
            id='win-percentage',
            figure = fig
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


