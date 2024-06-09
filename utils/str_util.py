'''
Clean a string from the following elements:
- Spaces at the start of the string

@param "string" : a string
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