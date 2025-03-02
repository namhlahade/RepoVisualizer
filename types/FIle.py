import PythonFunction

class File:
    def __init__(self, path):
        self.path = path
        self.lines = []
        self.parse_file()
        self.funcs = []
        self.classes = []
