"""
calls the correct parser for each file in the repository based on the file extension
:input: root directory of the repository
:output: list of filenames
"""
import os
import PythonParser

def parse_repo(repo_path):
    filenames = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py'):
                PythonParser.parse_python(os.path.join(root, file))
                filenames.append(os.path.join(root, file))
    return filenames

print(parse_repo("C:\\Users\\ayonb\\Documents\\Programs\\HackathonProjectSearch"))
