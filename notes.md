
1) read each file in a directory and get info about the opjects and functions
    - need operation to get each file in the repo and pass it to the correct parser
    - first get all classes in each file and then check for funtions in those classes or in the file itself
    - should get function name, params, return, and description if available
    - then get all object creations and function calls from each function for the connections
    - should note what libraries are imported and what functions are called from those libraries

2) store the connections in a graph

3) generate descriptions for the functions missing them
    - pass the child functions in the graph as context to the parent function

3) produce documentation for the codebase and a graph depicting the connections
