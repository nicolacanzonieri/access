'''
STR UTIL

Index:
- clean_str()
- str_to_char_list()
'''


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