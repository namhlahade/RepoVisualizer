from ..types.File import File
from ..types.PythonClass import PythonClass
from ..types.PythonMethod import PythonMethod


def parse_class(name:str, lines:list[str]) -> PythonClass:
    dec_line = lines.pop(0)
    class_name:str = dec_line[0].split(" ")[1].split("(")[0]
    params:list[(str, str)] = []
    description:str = ""

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

    while len(lines) > 0:
        line = lines.pop(0)
        #




def parse_python(file_path) -> File:
    with open(file_path, 'r') as file:
        f = File(file_path)
        lines = file.readlines()
        f.add_lines(lines)

    # break the file into methods and classes
    while len(lines) > 0:
        line = lines.pop(0)
        if line.startswith("class "):
            class_name:str = line.split(" ")[1].split("(")[0]
            class_lines:list[str] = []

            while len(lines) > 0:
                line = lines.pop(0)
                if line.startswith("    "):
                    class_lines.append(line[1:-1])
                else:
                    break

            class_ = parse_class(class_name, class_lines)
            f.add_class(class_)
