from type.PythonMethod import PythonMethod
from type.PythonClass import PythonClass

class File:
    def __init__(self, path):
        self.path:str = path
        self.lines:list[str] = []
        self.methods:list[PythonMethod] = []
        self.classes:list[PythonClass] = []

    def add_lines(self, lines):
        self.lines = lines

    def add_method(self, method:PythonMethod):
        self.methods.append(method)

    def add_class(self, class_:PythonClass):
        self.classes.append(class_)
