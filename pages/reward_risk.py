import dash_html_components as html

from pages.page import Page

page = Page("Reward-Risk")
page.set_path('/pages/reward_risk')

page.layout = html.Div([
    html.H1(page.name),
    html.Div(id=page.id + '-content'),
])
