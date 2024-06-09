import os


'''
Get the path separator for the current OS
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