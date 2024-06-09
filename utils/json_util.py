'''
JSON UTIL

Index:
- json_to_vec()
- print_json_vec()
'''


from utils.char_util import its_a_letter, its_a_number
from utils.vec_util import print_vec
from utils.str_util import clean_str


'''
Returns a vector with the elements of a JSON file.
@param path_to_json: the path to a specific JSON file.
'''
def json_to_vec(path_to_json) -> list:
    json_vec = []
    its_data = False
    push_to_subvec = False

    with open(path_to_json, "r") as json_file:
        line = json_file.read() # line is a string that contains the whole json file
        json_data = "" # Initialize json_data
        json_subvec = [] # Initialize json sub-vector

        for char in line: # Analyze each character of the json file
            if (its_a_letter(char) or its_a_number(char) or char == ' ') and its_data: # Current char it's part of a data
                json_data += str(char)
            elif char == ':': # The following chars are part of a data
                its_data = True
            elif char == '[': # There is a vector inside the JSON file
                push_to_subvec = True
                json_subvec = []
            elif char == "]": # End of the vector
                its_data = False
                push_to_subvec = False
                json_vec.append(json_subvec)
            elif char == chr(10): # Current char is NEW LINE FEED
                if clean_str(json_data) != "":
                    if push_to_subvec:
                        json_subvec.append(clean_str(json_data))
                        json_data = ""
                    else:
                        json_vec.append(clean_str(json_data))
                        json_data = ""
                        its_data = False
    return json_vec

'''
Print a json vector on terminal
@param "path_to_json" : the path to a specific JSON file.
'''
def print_json_vec(path_to_json):
    json_vec = json_to_vec(path_to_json)
    print_vec(json_vec)