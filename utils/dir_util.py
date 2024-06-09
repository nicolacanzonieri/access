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
    full_path = full_path[1:]
    return full_path


'''
Return a string containing the parent path for a given path
@param "current_path" : the path where the parent folder will be extracted
'''
def get_prnt_folder(current_path) -> str:
    path_len = len(current_path)
    index = path_len
    while index > 0:
        if current_path[index-1 : index] == get_path_separator():
            return current_path[0 : index]
        index -= 1
    return ""


'''
Return true if a certain file or directory exist in the given path
@param "path" : a string containing the path to a directory or a file
'''
def check(path) -> bool:
    return os.path.exists(path)


'''
Crate a new file in the given path
@param "path" : a string containing the path to the new file (this path must contain the filename with extension)
'''
def create_file(path):
    with open(path, "w") as new_file:
        new_file.write("")
        new_file.close()