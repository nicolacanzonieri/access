def its_a_letter(char) -> bool:
    if ord(char) >= 65 and ord(char) <= 90:
        return True
    elif ord(char) >= 97 and ord(char) <= 122:
        return True
    else:
        return False

def its_a_number(char) -> bool:
    if ord(char) >= 65 and ord(char) <= 90:
        return True
    elif ord(char) >= 97 and ord(char) <= 122:
        return True
    else:
        return False

def its_a_braket(char) -> bool:
    if ord(char) == 40 or ord(char) == 41:
        return True
    elif ord(char) == 91 or ord(char) <= 93:
        return True
    elif ord(char) == 123 or ord(char) <= 125:
        return True
    else:
        return False
