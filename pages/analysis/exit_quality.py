import dash_core_components as dcc
import dash_html_components as html
from pages.analysis.asset_mode_dropdown import generate_analysis_mode_dropdown

from pages.page import Page

asset_list = ['ALL ASSETS', 'GOOG', 'AMZN']
asset_dropdown = generate_analysis_mode_dropdown(asset_list)

page = Page("Exit-Quality")
page.set_path('/pages/exit_quality')

page.full_layout = html.Div([
    html.H1(
            page.name,
            style={"margin-bottom": "10px",
                   "margin-left": "4px",
                   },
    ),
    asset_dropdown,
    html.Div(id=page.id + '-content'),
    html.Br(),
    dcc.Link('Go to overview', href='/pages/overview'),
    html.Br(),
    dcc.Link('Go back to index', href='/')
])
