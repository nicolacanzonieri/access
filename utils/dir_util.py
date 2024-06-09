'''
DIR UTIL

Index:
- get_path_separator()
- get_path_to()
- check()
'''


import os


'''
Return the path separator (str) for the current OS
'''
def get_path_separator() -> str:
    return os.sep


'''
Return the os' accepted path (str) to a specified file with the correct path separator
@param "path_to_file" : a string that represent the path to a certain file with the following sintax:
                        path_to_file = "folder1 folder2 folder3 ... file"
'''
def get_path_to(path_to_file) -> str:
    path_vec = path_to_file.split()
    full_path = ""

    for item in path_vec:
        full_path = full_path + get_path_separator() + item
    full_path = "." + get_path_separator() + full_path
    
    return full_path


'''
Return true if a certain file or directory exist in the given path
@param "path" : a string containing the path to a directory or a file
'''
def check(path) -> bool:
    return os.path.exists(path)