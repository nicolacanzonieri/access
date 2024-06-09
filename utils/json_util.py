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
        line = json_file.read() # line is a string that contains the whole json file
        json_data = "" # Initialize json_data

        for char in line: # Analyze each character of the json file
            # If the char it's number/letter/'space'..
            if its_a_letter(char) or its_a_number(char) or char == ' ':
                json_data += str(char) # Add char to the data
                for parameter in parameters.split(): # Delete the parameters name from the data
                    if json_data == parameter:
                        json_data = ""
            elif char == chr(10): # if char it's new line feed...
                # If the data is not an empty string than it's a real data and can be added to the vec
                if clean_str(json_data) != "":
                    json_vec.append(clean_str(json_data))
                    json_data = ""
    print_vec(json_vec)