'''
JSON UTIL

Index:
- json_to_vec()
- edit_json()
- get_json_value()
- print_json_vec()
'''


from utils.char_util import its_a_letter, its_a_number
from utils.vec_util import print_vec
from utils.str_util import str_to_vec
from utils.file_util import file_to_vec, vec_to_file


'''
Returns a vector with the elements of a JSON file.
@param path_to_json: the path to a specific JSON file.

NOTE:
At the moment json_to_vec does not support lists in JSON files
'''
def json_to_vec(path_to_json) -> list:
    json_vec = []
    
    with open(path_to_json, "r") as json_file:
        line = json_file.read()
        line_vec = str_to_vec(line)
        vec_index = 0
        while vec_index < len(line_vec):
            line_len = len(line_vec[vec_index])
            line_index = line_len - 1
            while line_index >= 3 and vec_index < len(line_vec)-2:
                line = line_vec[vec_index]   
                if line[line_index : line_index + 1] == '"' and line[line_index-2 : line_index - 1] == ':' and line[line_index-3 : line_index - 2] == '"':
                    json_vec.append(line_vec[vec_index][line_index + 1 : line_len-2])
                    break
                line_index -= 1
            while line_index >= 3 and vec_index == len(line_vec)-2:
                line = line_vec[vec_index]   
                if line[line_index : line_index + 1] == '"' and line[line_index - 2 : line_index - 1] == ':' and line[line_index-3 : line_index - 2] == '"':
                    json_vec.append(line_vec[vec_index][line_index + 1 : line_len-1])
                    break
                line_index -= 1
            vec_index += 1
        
    return json_vec


'''
Edit a json file with a different value in a specified row
@param "path_to_json" : a string containing the path to a .json file
@param "row" : the row where to insert the new value. Remember that rows start from 0!
@param "new_value" : the new value to insert. This parameter must have the following syntax: '"Example"'
'''
def edit_json(path_to_json, row, new_value):
    file_vec = file_to_vec(path_to_json)
    for char_index, char in enumerate(file_vec[row]):
        if file_vec[row][char_index] == ':':
            file_vec[row] = file_vec[row][: char_index + 1] + " " + new_value
            # If the json contains multiple values and the modified row is not the last one (containing data)
            # than we have to add the ',' character at the end of the data
            if len(file_vec) > 3 and row < len(file_vec) - 2:
                file_vec[row] += ","
            break
    vec_to_file(path_to_json, file_vec)


'''
Return a string containing the value of a json value in a given row:
@param "path_to_json" : a string containing the path to a .json file
@param "value_id" : the number of the data (eg. the first value have id = 0, the second one have id = 1, ect...)
'''
def get_json_value(path_to_json, value_id) -> str:
    json_vec = json_to_vec(path_to_json)
    return json_vec[value_id]
            

'''
Print a json vector on terminal
@param "path_to_json" : the path to a specific JSON file.
'''
def print_json_vec(path_to_json):
    json_vec = json_to_vec(path_to_json)
    print_vec(json_vec)