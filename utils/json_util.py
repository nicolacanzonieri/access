from utils.char_util import its_a_letter, its_a_number
from utils.vec_util import print_vec

def json_to_vec(path_to_json):
    json_vec = []
    with open(path_to_json, "r") as json_file:
        line = json_file.read()
        new_data = ""
        for char in line:
            if its_a_letter(char) or its_a_number(char):
                new_data += str(char)
        json_vec.append(new_data)
    print_vec(json_vec)
    # TODO!