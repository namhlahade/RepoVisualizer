from backend.models import LanguageMethod

class LanguageClass:
    def __init__(self):
        self.name:str = ""
        self.methods:list[LanguageMethod] = [] # type: ignore

    def get_name(self) -> str:
        return self.name
    
    def add_name(self, name:str) -> None:
        self.name = name

    def get_methods(self) -> list[LanguageMethod]: # type: ignore
        return self.methods

    def add_methods(self, methods:list[LanguageMethod]) -> None: # type: ignore
        self.methods.append(methods)
