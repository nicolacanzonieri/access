'''
CHAR UTIL

Index:
- its_a_letter()
- its_a_number()
- its_a_bracket()
'''


'''
Return true if the given char is a letter
'''
def its_a_letter(char) -> bool:
    return 'A' <= char <= 'Z' or 'a' <= char <= 'z'


'''
Return true if the given char is a number
'''
def its_a_number(char) -> bool:
    return '0' <= char <= '9'


'''
Return true if the given char is a bracket
'''
def its_a_bracket(char) -> bool:
    return char in '()[]{}'
