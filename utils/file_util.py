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
    

'''
Return a list where each element is a sentence that in the file ends with the "new line feed" character.
@param "path_to_file" : a string containing the path to a file
'''
def file_to_vec(path_to_file) -> list:
    file_line = get_file(path_to_file)
    file_vec = []
    sub_file_line = ""
    char_index = 0

    if file_line[len(file_line) - 1 : len(file_line)] != "\n":
        file_line += "\n"

    while char_index < len(file_line):
        if file_line[char_index : char_index + 1] != "\n":
            sub_file_line += file_line[char_index : char_index + 1]
        else:
            file_vec.append(sub_file_line)
            sub_file_line = ""
        char_index += 1
    return file_vec