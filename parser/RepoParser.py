"""
calls the correct parser for each file in the repository based on the file extension
:input: root directory of the repository
:output: list of filenames
"""
import os
from parser.PythonParser import PythonParser

def parse_repo(repo_path: str) -> list:
    files = []

    for root, dirs, filenames in os.walk(repo_path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if filename.endswith('.py'):
                parser = PythonParser(file_path)
                files.append(parser.parse_python())
    return files

if __name__ == '__main__':
    print(parse_repo("/Users/namhlahade/Documents/GitHub/DukeNutrition"))
