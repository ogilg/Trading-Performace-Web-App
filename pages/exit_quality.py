import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from pages.page import Page
from app import app
page = Page("Exit-Quality")
page.set_path('/pages/exit_quality')

page.layout = html.Div([
    html.H1(page.name),
    html.Div(id= page.id + '-content'),
    html.Br(),
    dcc.Link('Go to overview', href='/pages/overview'),
    html.Br(),
    dcc.Link('Go back to index', href='/')
])
