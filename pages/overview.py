import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pages.page import Page

from app import app

page = Page('Overview')
page.set_path('/pages/overview')

page.layout = html.Div(children=[
    html.H1(children=page.name),
    html.Div(children='''
            Trading activity overview.
        '''),
    html.Br(),
    dcc.Link('Go to Page 2', href='page-2'),
    html.Br(),
    dcc.Link('Go back to index', href='/'),
    ])