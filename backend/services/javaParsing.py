import re

file_path = '/Users/namhlahade/Documents/Calculator.java'

class_pattern = re.compile(r'\bclass\s+(\w+)')

method_pattern = re.compile(r'public|protected|private|static|\s'
                            r'([\w<>\[\]]+\s+)+?'
                            r'(\w+)\s*\(([^)]*)\)',
                            re.VERBOSE)

def parse_parameters(param_string):
    params = param_string.split(',')
    param_details = []
    for param in params:
        if param:
            parts = param.strip().split(' ')
            param_type = ' '.join(parts[:-1])
            param_name = parts[-1]
            param_details.append((param_name, param_type))
    return param_details

with open(file_path, 'r') as file:
    content = file.read()

class_match = class_pattern.search(content)

class_name = None
if class_match:
    class_name = class_match.group(1)

methods = method_pattern.findall(content)

method_details = []
for return_type, method_name, params in methods:
    if method_name != class_name:
        param_details = parse_parameters(params)
        method_details.append({
            'method_name': method_name,
            'return_type': return_type.strip(),
            'parameters': param_details
        })

print(f"Class Name: {class_name}\n")

for method in method_details:
    print(f"Method Name: {method['method_name']}")
    print(f"Return Type: {method['return_type']}")
    print("Parameters:")
    for name, type in method['parameters']:
        print(f"  {name} : {type}")
    print("\n")