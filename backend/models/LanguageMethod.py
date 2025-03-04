class LanguageMethod:
    def __init__(self):
        self.method_name:str = ""
        self.return_type:str = ""
        self.parameters:list[str] = []

    def get_method_name(self) -> str:
        return self.method_name 
    
    def add_method_name(self, method_name:str) -> None:
        self.method_name = method_name

    def get_return_type(self) -> str:
        return self.return_type
    
    def add_return_type(self, return_type:str) -> None:
        self.return_type = return_type

    def get_parameters(self) -> list[str]:
        return self.parameters
    
    def add_parameters(self, parameters:list[str]) -> None:
        self.parameters.append(parameters)
