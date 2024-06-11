'''
FILE UTIL

Index:
- print_file()
'''


'''
Print a file on a specified path, on terminal
@param "path_to_file" : a string containing the path to a file
'''
def print_file(path_to_file):
    with open(path_to_file, "r") as file:
        file_lines = file.read()
        print(file_lines)
    # TODO!