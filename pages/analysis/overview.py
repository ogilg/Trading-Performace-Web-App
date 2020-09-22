import dash_html_components as html
from pages.analysis.asset_mode_dropdown import generate_analysis_mode_dropdown

from pages.page import Page

page = Page('Overview')
page.set_path('/analysis/overview')

asset_list = ['ALL ASSETS', 'GOOG', 'AMZN']
asset_dropdown = generate_analysis_mode_dropdown(asset_list)
overview_metrics = ['p&l', 'rate-of-return']

page.set_storage(overview_metrics)

page.set_layout(html.Div([
        html.H1(
            page.name,
            style={"margin-bottom": "10px",
                   "margin-left": "4px",
                   },
        ),

        html.Div(children='''
            Trading activity overview.
        '''),
        asset_dropdown,
]))
