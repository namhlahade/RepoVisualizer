"""
calls the correct parser for each file in the repository based on the file extension
:input: root directory of the repository
:output: list of filenames
"""
import os
from parser.PythonParser import PythonParser

def parse_repo(repo_path: str) -> list:
    files = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.py'):
                parser = PythonParser(file_path)
                file = parser.parse_python()
                files.append(file_path)
    return files

if __name__ == '__main__':
    print(parse_repo("C:\\Users\\ayonb\\Documents\\Programs\\HackathonProjectSearch"))
