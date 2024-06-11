'''
FILE UTIL

Index:
- print_file()
'''


'''
Print a file located on a specified path, on terminal
@param "path_to_file" : a string containing the path to a file
'''
def print_file(path_to_file):
    with open(path_to_file, "r") as file:
        file_lines = file.read()
        print(file_lines)


'''
Return a string containing a text file located on a specified path
@param "path_to_file" : a string containing the path to a file
'''
def get_file(path_to_file) -> str:
    with open(path_to_file, "r") as file:
        file_lines = file.read()
        return file_lines