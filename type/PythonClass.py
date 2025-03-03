class PythonClass:
    def __init__(self, name:str, params:list[(type, str)], description:str):
        self.name:str = name
        self.params:list[(str, str)] = params
        self.lines:list[str] = []
        self.description:str = description

        self.calls:list = []

    def add_lines(self, lines):
        self.lines = lines
