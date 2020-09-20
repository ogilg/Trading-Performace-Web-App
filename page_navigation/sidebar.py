import dash_bootstrap_components as dbc
import dash_html_components as html

from pages.analysis import overview, exit_quality, reward_risk, win_loss


class SideBar:
    def __init__(self, style):
        self.style = style

    def set_pages(self, pages):
        # dict with name to display and Page object
        self.pages = pages

    def create_page_links(self):
        page_links = []
        for page_name in self.pages:
            page_links.append(
                dbc.NavLink(page_name.page.name, href=page_name.page.path, id=page_name.page.id,
                            style={'color': 'white'}))
            page_links.append(html.Br())
        return page_links

    def create_layout(self):
        page_links = self.create_page_links()
        self.layout = self.get_layout_html(page_links)

    def get_layout_html(self, page_links):
        layout = html.Div(
            [
                html.H5("Trade Performance Analysis", className="display-5", style={'color': 'white'}),
                html.Hr(),

                dbc.Nav(
                    page_links,
                    vertical=True,
                    pills=True,
                ),
            ],
            style=self.style,
            className="pretty_container",
        )
        return layout


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 59,
    "left": 0,
    "bottom": 0,
    "width": "13rem",
    "padding": "1rem 1rem",
    "background-color": "#1218de",
}
pages = [overview, win_loss, reward_risk, exit_quality]

sidebar = SideBar(SIDEBAR_STYLE)
sidebar.set_pages(pages)
sidebar.create_layout()
