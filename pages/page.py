import dash_core_components as dcc
import dash_html_components as html


class Page:
    def __init__(self, name):
        self.name = name
        self.id = name.lower()
        self.storage = html.Div([])

    def set_path(self, path):
        self.path = path

    def set_storage(self, stored_data_list):
        self.storage = html.Div([dcc.Store(id='-'.join((self.id, stored_metric)), storage_type='session') for stored_metric in stored_data_list], id=self.id+'storage')

    def set_layout(self, layout):
        self.layout = html.Div([self.storage, layout])

    def get_layout(self):
        return self.layout
