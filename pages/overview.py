import dash_html_components as html

from pages.page import Page

page = Page('Overview')
page.set_path('/pages/overview')

page.layout = html.Div(children=[
    html.H1(children=page.name),
    html.Div(children='''
            Trading activity overview.
        '''),
])
