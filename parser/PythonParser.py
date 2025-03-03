
from type.File import File
from type.PythonClass import PythonClass
from type.PythonMethod import PythonMethod


def parse_class(lines:list[str]) -> tuple[PythonClass, list[str]]:
    dec_line = lines.pop(0)
    class_name:str = dec_line[0].split(" ")[1].split("(")[0]
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
    while len(lines) > 0:
        line = lines.pop(0)
        if line.startswith(("    ", "\t", " ", "\n")):
            # remove the leading tab wether it is 4 spaces or a tab
            print(len(line), end=", ")
            print(len(line.lstrip()))
        else:
            break




def parse_python(file_path) -> File:
    with open(file_path, 'r') as file:
        f = File(file_path)
        lines: list[str] = file.readlines()
        f.add_lines(lines)

    # break the file into methods and classes
    while len(lines) > 0:
        line = lines.pop(0)
        if line.startswith("class "):
            class_, lines = parse_class(lines)
            f.add_class(class_)
