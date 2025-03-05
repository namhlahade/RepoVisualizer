import re
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


    def _parse_object(self, obj:str) -> str:
        obj = obj.strip()
        print("parsing object", obj)
        objs = obj.split(".")
        if objs[0] in self.objects:
            self.objects[".".join(objs[1:])] = objs[0]
        while objs[0] in self.objects:
            objs.insert(0, self.objects[objs[0]])
            if objs[0] == ".":
                break
        print("objs", objs)
        return ".".join(objs)

    def _parse_params(self, line:str) -> list[(str, str)]:
        params:list[(str, str)] = []
        start_params = line.find("(")
        end_params = line.rfind(")")
        if start_params != -1 and end_params != -1:
            param_strs = line[start_params + 1:end_params].split(", ")
            for param_str in param_strs:
                param_str = param_str.strip()
                if param_str.__contains__("="):
                    param_str, obj = param_str.split("=")
                    obj = self._parse_object(obj)
                    print("obj", obj)
                else:
                    obj = "."
                if param_str.__contains__(":"):
                    param, type_ = param_str.split(":")
                else:
                    param = param_str
                    type_ = None
                param = param.strip()
                type_ = type_.strip() if type_ is not None else None
                obj = obj.strip()
                params.append((param, type_))
                self.objects[param] = obj
                print(self.objects)
        return params

    def _parse_method(self, current_name:str, indent:int) -> PythonMethod:
        dec_line = self.lines.pop(0)
        method_name:str = current_name + "." + dec_line[dec_line.find("def ") + 4:dec_line.find("(")]
        print(f"parsing method {method_name}")
        description:str = ""
        params:list[(str, str)] = self._parse_params(dec_line)
        print("params", params)

        method_lines:list[str] = []
        while len(self.lines) > 0:
            line = self.lines[0]
            if line.startswith(("    " * indent, "\n")):
                method_lines.append(line[(indent + 1) * 4:])
            else:
                break
            self.lines.pop(0)
        return PythonMethod(method_name, description, params, method_lines)

    def _parse_class(self, current_name:str, indent:int) -> PythonClass:
        dec_line = self.lines.pop(0)
        class_end = min(i for i in (dec_line.find("("), dec_line.find(":")) if i != -1)
        class_name:str = current_name + "." + dec_line[dec_line.find("class ") + 6:class_end]
        print(print(f"parsing class {class_name}"))
        description:str = ""
        params:list[(str, str)] = self._parse_params(dec_line)

        class_lines:list[str] = []
        while len(self.lines) > 0:
            line = self.lines[0]
            if line.startswith(("    " * (indent + 1), "\n")):
                class_lines.append(line[(indent + 1) * 4:])
                if line.__contains__("def "):
                    method = self._parse_method(class_name, indent + 1)
                    self.file.add_method(method)
                    print("method")
                elif line.__contains__("class "):
                    class_ = self._parse_class(class_name, indent + 1)
                    self.file.add_class(class_)

            else:
                break
            self.lines.pop(0)

    def parse_python(self) -> File:
        print(f"parsing {self.file_path}")
        # break the file into methods and classes
        while len(self.lines) > 0:
            line = self.lines[0]
            if line.startswith("class "):
                class_ = self._parse_class("", 0)
                self.file.add_class(class_)
            if line.startswith("from "):
                source = line[5:line.find(" import")].strip()
                imports = line[line.find("import ") + 7:].split(", ")
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
