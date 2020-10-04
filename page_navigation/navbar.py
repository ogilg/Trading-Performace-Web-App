import dash_bootstrap_components as dbc
import dash_html_components as html
from PIL import Image

GAMMA_IMAGE = Image.open(r'C:\Users\oscar\PycharmProjects\Trading-Performace-Web-App\images\gamma.png')
from pages import trade_journal
from pages.analysis import overview


class NavBar:
    def __init__(self):
        #self.create_search_bar()
        pass

    def set_main_pages(self, main_pages):
        # dict with name to display and Page object
        self.main_pages = main_pages

    def create_columns(self):
        self.columns = [dbc.Col(html.A(html.Img(src=GAMMA_IMAGE, height="35px"), href="https://icons8.com", ))]
        for main_page_key in self.main_pages:
            self.columns.append(dbc.Col(
                dbc.NavItem(dbc.NavLink(main_page_key, href=self.main_pages[main_page_key].page.path,
                                        className='navbar_columns', style={'fontSize': 20})),
                width=30
            ))
        return self.columns

    # def create_search_bar(self):
    #     self.search_bar = dbc.Row(
    #         [
    #             dbc.Col(dbc.Input(type="search", placeholder="Search")),
    #             dbc.Col(
    #                 dbc.Button("Search", color="primary", className="ml-2"),
    #                 width="auto",
    #             ),
    #         ],
    #         no_gutters=True,
    #         className="ml-auto flex-nowrap mt-3 mt-md-0",
    #         align="center",
    #     )

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
            ],
            color="dark",
            dark=True,
            className='navbar'
        )
        return layout



main_pages = {'Performance Analysis': overview, 'Trading Journal': trade_journal}

navbar = NavBar()
navbar.set_main_pages(main_pages)
navbar.create_layout()
