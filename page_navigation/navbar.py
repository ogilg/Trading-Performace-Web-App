import dash_bootstrap_components as dbc
import dash_html_components as html
from PIL import Image

GAMMA_IMAGE = Image.open(r'C:\Users\oscar\PycharmProjects\Trading-Performace-Web-App\images\gamma.png')
from pages import overview, trade_journal


class NavBar:
    def __init__(self, style, columns_style):
        self.style = style
        self.columns_style = columns_style
        self.create_search_bar()

    def set_main_pages(self, main_pages):
        # dict with name to display and Page object
        self.main_pages = main_pages

    def create_columns(self):
        self.columns = [dbc.Col(html.A(html.Img(src=GAMMA_IMAGE, height="35px"), href="https://icons8.com", ))]
        for main_page_key in self.main_pages:
            self.columns.append(dbc.Col(
                dbc.NavItem(dbc.NavLink(main_page_key, href=self.main_pages[main_page_key].page.path,
                                        style=self.columns_style)),
                width=30
            ))
        return self.columns

    def create_search_bar(self):
        self.search_bar = dbc.Row(
            [
                dbc.Col(dbc.Input(type="search", placeholder="Search")),
                dbc.Col(
                    dbc.Button("Search", color="primary", className="ml-2"),
                    width="auto",
                ),
            ],
            no_gutters=True,
            className="ml-auto flex-nowrap mt-3 mt-md-0",
            align="center",
        )

    def create_layout(self):
        columns = self.create_columns()
        self.layout = self.get_layout_html(columns)

    def get_layout_html(self, columns):
        layout = dbc.Navbar(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        columns,
                        align="center",
                        no_gutters=True,
                    ),
                ),
                dbc.NavbarToggler(id="navbar-toggler"),
                dbc.Collapse(self.search_bar, id="navbar-collapse", navbar=True),
            ],
            color="dark",
            dark=True,
            style=self.style,
        )
        return layout


style = {
    'top': 0,
    'left': 0,
    "position": "fixed",
    'width': '100%',
    'height': '8%',
}
columns_style = {'color': 'white', 'fontSize': 20, 'padding-bottom': '8%', 'padding-left': '100px'}
main_pages = {'Performance Analysis': overview, ' Trading Journal': trade_journal}

navbar = NavBar(style, columns_style)
navbar.set_main_pages(main_pages)
navbar.create_layout()
