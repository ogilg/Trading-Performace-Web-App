import dash_core_components as dcc
import dash_html_components as html


class Page:
    def __init__(self, name):
        self.name = name
        self.id = name.lower()

    def set_path(self, path):
        self.path = path

    def set_layout_with_storage(self, layout):
        self.layout = html.Div(
            [
                dcc.Store(id='-'.join((self.id, 'data')), storage_type='local'),
                layout
            ]
        )

    def get_layout(self):
        return self.layout
