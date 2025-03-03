class PythonMethod:
    def __init__(self, name:str, params:list[(type, str)], return_type:type, description:str):
        self.name:str = name
        self.params:list[(type, str)] = params
        self.return_type: type = return_type
        self.lines:list[str] = []
        self.description:str = description

        self.calls:list = []
