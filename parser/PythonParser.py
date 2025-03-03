
from type.File import File
from type.PythonClass import PythonClass
from type.PythonMethod import PythonMethod

class PythonParser:
    def __init__(self, file_path:str):
        self.file_path:str = file_path
        self.file = File(file_path)
        self.objects:list[dict[str,str]] = []


        with open(self.file_path, 'r') as file:
            self.lines: list[str] = file.readlines()
            self.file.add_lines(self.lines)

    def _parse_class(self) -> PythonClass:
        dec_line = self.lines.pop(0)
        class_name:str = dec_line[dec_line.find("class ") + 6:dec_line.find("(")]
        print(class_name)
        description:str = ""

        params:list[(str, str)] = []
        start_params = dec_line.find("(")
        end_params = dec_line.rfind(")")
        if start_params != -1 and end_params != -1:
            param_strs = dec_line[start_params + 1:end_params].split(", ")
            for param_str in param_strs:
                param = param_str.split(":")
                if len(param) == 2:
                    params.append((param[0], param[1]))
                else:
                    params.append((None, param[0]))

        class_lines:list[str] = []
        while len(self.lines) > 0:
            line = self.lines[0]
            if line.startswith(("    ", "\t", "    ", "\n")):
                class_lines.append(line[4:])
            else:
                break
            self.lines.pop(0)


    def parse_python(self) -> File:
        print(f"parsing {self.file_path}")
        # break the file into methods and classes
        while len(self.lines) > 0:
            line = self.lines[0]
            if line.startswith("class "):
                class_ = self._parse_class()
                self.file.add_class(class_)
            self.lines.pop(0)
        return self.file
