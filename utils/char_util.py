def its_a_letter(char) -> bool:
    return 'A' <= char <= 'Z' or 'a' <= char <= 'z'

def its_a_number(char) -> bool:
    return '0' <= char <= '9'

def its_a_bracket(char) -> bool:
    return char in '()[]{}'
