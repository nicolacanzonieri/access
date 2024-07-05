'''
STR UTIL

Index:
- clean_str()
- str_to_char_list()
- str_to_vec()
- str_to_int()
'''


import math


'''
Return a string cleaned from the following "mistakes":
 - Spaces at the start of the string

@param "string" : a string to clean
'''
def clean_str(string) -> str:
    better_str = ""
    str_index = 0
    spaces_at_the_start = True

    while str_index < len(string):
        if spaces_at_the_start:
            if string[str_index : str_index + 1] == " ":
                # The first chars of the string are 'space'
                better_str = better_str
            else:
                better_str += string[str_index : str_index + 1]
                spaces_at_the_start = False
        else:
            better_str += string[str_index : str_index + 1]
        str_index += 1
    return better_str


'''
Return a vector where each cell is a character of a given string
@param "string" : the interested string
'''
def str_to_char_list(string) -> list:
    char_list = []
    str_index = 0
    while str_index < len(string):
        char_list.append(string[str_index : (str_index + 1)])
        str_index += 1
    return char_list
    

'''
Return a list where each element is a sentence that in the string ends with the "new line feed" character.
@param "string" : the interested string
'''
def str_to_vec(string) -> list:
    str_vec = []
    sub_file_line = ""
    char_index = 0

    if string[len(string) - 1 : len(string)] != "\n":
        string += "\n"

    while char_index < len(string):
        if string[char_index : char_index + 1] != "\n":
            sub_file_line += string[char_index : char_index + 1]
        else:
            str_vec.append(sub_file_line)
            sub_file_line = ""
        char_index += 1
    return str_vec


'''
Returns the result of converting a string to an integer.
@param string: A string containing only numbers.
'''
def str_to_int(string) -> int:
    char = string[0]
    if len(string) > 1:
        return (ord(char) - 48) * pow(10, (len(string) - 1)) + str_to_int(string[1:])
    else:
        return (ord(char) - 48)