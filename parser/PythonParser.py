import re
from type.File import File
from type.PythonClass import PythonClass
from type.PythonMethod import PythonMethod

class PythonParser:
    # todo: need to find function calls
    def __init__(self, file_path:str):
        self.file_path:str = file_path
        self.file = File(file_path)
        self.objects:dict[str,str] = {}
        # todo: need to store number of indents with the name to know when to pop each scope
        self.scope:list[PythonClass|PythonMethod|str] = ["."]
        self.doc_string = None

        with open(self.file_path, 'r') as file:
            self.lines: list[str] = file.readlines()
            self.file.add_lines(self.lines)


    def _parse_object(self, obj:str) -> str:
        # todo: need to handle nested objects
        obj = obj.strip()
        print("----parsing object", obj)

        # check if the parent object has already been parsed
        objs = obj.split(".")
        if objs[0] in self.objects:
            self.objects[".".join(objs[1:])] = objs[0]
            objs.pop(0)

        # make full trace of object
        while objs[0] in self.objects:
            objs.insert(0, self.objects[objs[0]])
            if objs[0] == ".":
                break
        return ".".join(objs)

    def _parse_params(self, line:str) -> list[(str, str)]:
        params:list[(str, str)] = []

        # find params between parentheses
        start_params = line.find("(")
        end_params = line.rfind(")")
        if start_params != -1 and end_params != -1:
            # iterate through each param
            param_strs = line[start_params + 1:end_params].split(", ")
            print("---parsing params", param_strs)
            for param_str in param_strs:
                param_str = param_str.strip()

                # handle value being assigned to param
                if param_str.__contains__("="):
                    param_str, obj = param_str.split("=")
                    obj = self._parse_object(obj)
                    print("obj", obj)
                else:
                    obj = "."

                # handle type declaration
                if param_str.__contains__(":"):
                    param, type_ = param_str.split(":")
                else:
                    param = param_str
                    type_ = None

                # remove whitespace and add to lists
                param = param.strip()
                type_ = type_.strip() if type_ is not None else None
                obj = obj.strip()
                params.append((param, type_))
                self.objects[param] = obj
        return params

    def _parse_line(self, indent:int):
        line = self.lines[0]
        print(self.scope[-1], line, end="")
        line = line.split("#")[0]
        # todo: handel doc strings (remember need to look for both " and ' and need to keep track of which is being used to look for the closing quotes)
        # find the index of the starting quote then ignore the rest of that line
        # ignore each other line until the corresponding closing quote is found
        if line.__contains__("'''") or line.__contains__('"""'):
            single_ind = line.find("'''")
            double_ind = line.find('"""')
            if single_ind != -1 and (double_ind == -1 or single_ind < double_ind):
                # handle single quotes
                line = line[:single_ind] + line[single_ind + 3:]
                self.doc_string = "'''"
        if line.__contains__("def "):
            # handle method
            method = self._parse_method(indent)
            self.file.add_method(method)
        elif line.__contains__("class "):
            # handle class
            class_ = self._parse_class(indent)
            self.file.add_class(class_)
        else:
            self.lines.pop(0)


    def _parse_method(self, indent:int) -> PythonMethod:
        dec_line = self.lines.pop(0)
        method_name:str = self.scope[-1] + "." + dec_line[dec_line.find("def ") + 4:dec_line.find("(")]
        print("--parsing method", method_name)
        description:str = ""
        params:list[(str, str)] = self._parse_params(dec_line)
        self.scope.append(method_name)

        # iterate through method lines
        method_lines:list[str] = []
        while len(self.lines) > 0:
            line = self.lines[0]
            # check if line is part of method
            if line.startswith(("    " * (indent + 1), "\n")):
                method_lines.append(line[(indent + 1) * 4:])
                self._parse_line(indent + 1)
            else:
                self.scope.pop()
                break
        return PythonMethod(method_name, description, params, method_lines)

    def _parse_class(self, indent:int) -> PythonClass:
        dec_line = self.lines.pop(0)
        class_end = min(i for i in (dec_line.find("("), dec_line.find(":")) if i != -1)
        class_name:str = self.scope[-1] + "." + dec_line[dec_line.find("class ") + 6:class_end]
        print("-parsing class", class_name)
        description:str = ""
        params:list[(str, str)] = self._parse_params(dec_line)
        self.scope.append(class_name)

        # iterate through class lines
        class_lines:list[str] = []
        while len(self.lines) > 0:
            line = self.lines[0]
            # iterate through class lines
            if line.startswith(("   " * (indent + 1), "\n")):
                # todo: just need to check if the line is a method, class or other
                # if its other then its basically part of init
                # todo: get info from init method to add to class params
                class_lines.append(line[(indent + 1) * 4:])
                self._parse_line(indent + 1)
            else:
                print("breaking on this line", line, "cause i want indent", indent)
                break

    def parse_python(self) -> File:
        print(f"parsing {self.file_path}")
        # break the file into methods and classes
        while len(self.lines) > 0:
            line = self.lines[0]
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
                self.lines.pop(0)
            elif line.startswith("import "):
                imports = line[7:].split(", ")
                for import_ in imports:
                    if import_.__contains__(" as "):
                        self.objects[import_[import_.find(" as ") + 4:].strip()] = import_[:import_.find(" as ")].strip()
                        self.objects[import_[:import_.find(" as ")].strip()] = "."
                    else:
                        self.objects[import_.strip()] = "."
                self.lines.pop(0)
            else:
                self._parse_line(0)
        print("found objects", self.objects)
        return self.file
