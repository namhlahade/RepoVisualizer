import re
from backend.models.LanguageClass import LanguageClass
from backend.models.LanguageMethod import LanguageMethod

file_path = '/Users/namhlahade/Documents/Calculator.java'

class_pattern = re.compile(r'\bclass\s+(\w+)')

method_pattern = re.compile(r'''
    (?:@[\w]+[\s]*)* 
    (public|protected|private|static|final|\s)+
    ([\w<>\[\]]+\s+)+                         
    (\w+)\s*                              
    \(([^)]*)\)                              
    ''', re.VERBOSE | re.DOTALL)

def parse_parameters(param_string):
    params = param_string.split(',')
    param_details = []
    for param in params:
        if param:
            parts = param.strip().split(' ')
            param_type = ' '.join(parts[:-1])
            param_name = parts[-1]
            param_details.append(f"{param_name}: {param_type}")
    return param_details

try:
    with open(file_path, 'r') as file:
        content = file.read()

    language_class = LanguageClass()
    class_match = class_pattern.search(content)
    if class_match:
        language_class.add_name(class_match.group(1))

    methods = method_pattern.findall(content)
    for modifiers, return_type, method_name, params in methods:
        if method_name != language_class.get_name():
            language_method = LanguageMethod()
            language_method.add_method_name(method_name)
            language_method.add_return_type(return_type.strip())
            parameter_details = parse_parameters(params)
            for param in parameter_details:
                language_method.add_parameters(param)
            language_class.add_methods(language_method)

    print(f"Class Name: {language_class.get_name()}")
    print(language_class.get_methods())
    for method in language_class.get_methods():
        print(f"Method Name: {method.get_method_name()}")
        print(f"Return Type: {method.get_return_type()}")
        print("Parameters:")
        for param in method.get_parameters():
            print(f"  {param}")
        print("\n")
except IOError:
    print("Error: File not found or unable to read file")
except Exception as e:
    print(f"An error occurred: {e}")
