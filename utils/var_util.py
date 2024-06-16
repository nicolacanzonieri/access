'''
VAR UTIL

Index:
- string_to_int()
'''


import math


'''
Returns the result of converting a string to an integer.
@param string: A string containing only numbers.
'''
def string_to_int(string) -> int:
    char = string[0]
    if len(string) > 1:
        return (ord(char) - 48) * pow(10, (len(string) - 1)) + string_to_int(string[1:])
    else:
        return (ord(char) - 48)