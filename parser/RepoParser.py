"""
calls the correct parser for each file in the repository based on the file extension
:input: root directory of the repository
:output: list of filenames
"""
import os
import PythonParser

def parse_repo(repo_path: str) -> list:
    filenames = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.py'):
                PythonParser.parse_python(file_path)
                filenames.append(file_path)
    return filenames

if __name__ == '__main__':
    print(parse_repo("C:\\Users\\ayonb\\Documents\\Programs\\HackathonProjectSearch"))
