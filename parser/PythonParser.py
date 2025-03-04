
from type.File import File
from type.PythonClass import PythonClass
from type.PythonMethod import PythonMethod

class PythonParser:
    def __init__(self, file_path:str):
        self.file_path:str = file_path
        self.file = File(file_path)
        self.objects:dict[str,str] = {}

        with open(self.file_path, 'r') as file:
            self.lines: list[str] = file.readlines()
            self.file.add_lines(self.lines)

    def _parse_params(self, line:str) -> list[(str, str)]:
        params:list[(str, str)] = []
        start_params = line.find("(")
        end_params = line.rfind(")")
        if start_params != -1 and end_params != -1:
            param_strs = line[start_params + 1:end_params].split(", ")
            for param_str in param_strs:
                param = param_str.split(":")
                if len(param) == 2:
                    params.append((param[1], param[0]))
                else:
                    params.append((param[0], None))
        return params

    def _parse_class(self, indent:int) -> PythonClass:
        dec_line = self.lines.pop(0)
        class_end = min(i for i in (dec_line.find("("), dec_line.find(":")) if i != -1)
        class_name:str = dec_line[dec_line.find("class ") + 6:class_end]
        print(print(f"parsing class {class_name}"))
        description:str = ""
        params:list[(str, str)] = self._parse_params(dec_line)

        class_lines:list[str] = []
        while len(self.lines) > 0:
            line = self.lines[0]
            if line.startswith(("    ", "\t", "    ", "\n")):
                class_lines.append(line[4:])
                if line.__contains__("def "):
                    method = self._parse_method(line)
                    self.file.add_method(method)
                elif line.__contains__("class "):
                    class_ = self._parse_class()
                    self.file.add_class(class_)

            else:
                break
            self.lines.pop(0)

    def _parse_object(self, obj:str) -> str:
        objs = obj.split(".")
        while objs[0] in self.objects:
            objs[0] = self.objects[objs[0]]
            if objs[0] == ".":
                break
        return ".".join(objs)


    def parse_python(self) -> File:
        print(f"parsing {self.file_path}")
        # break the file into methods and classes
        while len(self.lines) > 0:
            line = self.lines[0]
            if line.startswith("class "):
                class_ = self._parse_class()
                self.file.add_class(class_)
            if line.startswith("from "):
                imports = line[line.find("import ") + 7:].split(", ")
                source = line[5:line.find(" import")].strip()
                self.objects[source] = "."
                for import_ in imports:
                    if import_.__contains__(" as "):
                        self.objects[import_[import_.find(" as ") + 4:].strip()] = import_[:import_.find(" as ")].strip()
                        self.objects[import_[:import_.find(" as ")].strip()] = source
                    else:
                        self.objects[import_.strip()] = source
            if line.startswith("import "):
                imports = line[7:].split(", ")
                for import_ in imports:
                    if import_.__contains__(" as "):
                        self.objects[import_[import_.find(" as ") + 4:].strip()] = import_[:import_.find(" as ")].strip()
                        self.objects[import_[:import_.find(" as ")].strip()] = "."
                    else:
                        print("import", import_)
                        self.objects[import_.strip()] = "."
            self.lines.pop(0)
        print("objs", self.objects)
        return self.file
