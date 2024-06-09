from utils.char_util import its_a_letter, its_a_number
from utils.vec_util import print_vec
from utils.str_util import clean_str


'''
Returns a vector with the elements of a JSON file.
@param path_to_json: The path to a specific JSON file.
@param parameters: A string containing the names of the parameters in the JSON file
'''
def json_to_vec(path_to_json, parameters):
    json_vec = []
    with open(path_to_json, "r") as json_file:
        line = json_file.read()
        new_data = ""
        for char in line:
            if its_a_letter(char) or its_a_number(char) or char == ' ':
                new_data += str(char)
                for parameter in parameters.split(): # delete the parameter name
                    if new_data == parameter:
                        new_data = ""
            elif char == chr(10): # if char it's new line feed...
                if clean_str(new_data) != "":
                    json_vec.append(clean_str(new_data))
                    new_data = ""
    print_vec(json_vec)
    # TODO!