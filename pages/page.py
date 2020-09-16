class Page:
    def __init__(self, name):
        self.name = name
        self.id = name.lower()

    def set_path(self, path):
        self.path = path

