import dash_html_components as html
from pages.analysis.asset_mode_dropdown import generate_analysis_mode_dropdown

from pages.page import Page

page = Page('Overview')
page.set_path('/analysis/overview')

asset_list = ['ALL ASSETS', 'GOOG', 'AMZN']
sessions = ['session 1', 'session 2']
asset_dropdown = generate_analysis_mode_dropdown(asset_list, sessions)

page.set_layout_with_storage(html.Div([
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
