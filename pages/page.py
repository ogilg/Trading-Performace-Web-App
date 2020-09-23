import dash_html_components as html


class Page:
    def __init__(self, name):
        self.name = name
        self.id = name.lower()
        self.storage = []

    def set_path(self, path):
        self.path = path

    def set_storage(self, stored_data_list):
        self.storage = stored_data_list

    def set_layout(self, layout):
        self.layout = html.Div(layout)

    def get_layout(self):
        return self.layout
