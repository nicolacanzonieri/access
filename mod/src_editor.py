"""
SOURCE EDITOR


Index:
- get_key()
- clear_terminal()
- extend_file_vec()
- print_cursor()
- print_ui()
- input_handler()
- main_logic()
- start_editor()
"""

import sys
import os

from utils.file_util import file_to_vec
from utils.json_util import get_json_value
from utils.dir_util import get_path_to
from utils.str_util import str_to_int


"""
SYSTEM VARIABLES
"""
sys_var_json_path = get_path_to("json sys_var.json")
max_string_length = str_to_int(get_json_value(sys_var_json_path, 1))


'''
Detect special keys pressed by the user
'''
if sys.platform == "win32":
    import msvcrt

    def get_key():
        while True:
            key = msvcrt.getch()
            if key == b'\t':      # Up
                return "CTRL+I"
            elif key == b'\x0c':  # Right
                return "CTRL+L"
            elif key == b'\r':    # Down
                return "CTRL+M"
            elif key == b'\n':    # Left
                return "CTRL+J"
            elif key == b'\x0f':  # Fast right
                return "CTRL+O"
            elif key == b'\x15':  # Fast left
                return "CTRL+U"
            elif key == b'\x17':  # Close
                return "CTRL+W"
            elif key == b"\x08":  # Backspace/Delete key
                return "DELETE"
            elif key == b"\xe0":
                return "CANCEL"
            return key.decode("utf-8")

else:
    import tty
    import termios

    def get_key():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
            if ord(key) == 9:     # Up
                return "CTRL+I"
            elif ord(key) == 12:  # Right
                return "CTRL+L"
            elif ord(key) == 13:  # Down
                return "CTRL+M"
            elif ord(key) == 10:  # Left
                return "CTRL+J"
            elif ord(key) == 15:  # Fast right
                return "CTRL+O"
            elif ord(key) == 21:  # Fast left
                return "CTRL+U"
            elif ord(key) == 23:  # Close
                return "CTRL+W"
            elif ord(key) == 127:
                return "DELETE"
            elif ord(key) == 126:
                return "CANCEL"
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key


"""
Clear terminal
"""
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


'''
Returns a list of sentences extracted from the provided file, where each sentence is either shorter than or equal 
to the specified maximum length. Sentences exceeding the limit are split into multiple elements.
@param "file_vec" : The original list of strings representing file contents (potentially containing long sentences).
'''
def extend_file_vec(file_vec) -> list:
    vec_index = 0
    while vec_index < len(file_vec):
        line = file_vec[vec_index]
        print(line)
        if len(line) > max_string_length:
            file_vec[vec_index] = file_vec[vec_index][ : max_string_length]
            file_vec.insert(vec_index + 1, line[max_string_length : ])
        vec_index += 1
    return file_vec
        

"""
Print the cursor line with the cursor
@param "line" : the string that we are modifying
@param "cursor_x" : the cursor x position
"""
def print_cursor(line, cursor_x):
    line_index = 0
    
    while line_index <= len(line):
        if line_index == cursor_x:
            print("^", end="")
        else:
            print(" ", end="")
        line_index += 1
    print("")


"""
Print UI
@param "file_vec" : the list obtained from the file (file_to_vec)
@param "cursor_x" : cursor x position
@param "cursor_y" : cursor y position
"""
def print_ui(file_vec, cursor_x, cursor_y):
    file_vec_len = len(file_vec)
    file_vec_index = 0

    # PRINTER
    while file_vec_index < file_vec_len:
        if cursor_y == file_vec_index:
            is_cursor_line = True
        else:
            is_cursor_line = False

        file_line = file_vec[file_vec_index]
        print(file_line)

        if is_cursor_line:
            print_cursor(file_line, cursor_x)
        
        file_vec_index += 1


'''
Return a tuple containing the new cursor position after having analyzed user input
@param user_input: string containing pressed key/combination
@param "cursor_x" : cursor x position
@param "cursor_y" : cursor y position
'''
def input_handler(user_input, cursor_x, cursor_y) -> tuple:
    if user_input == "CTRL+I":
        cursor_y -= 1
    elif user_input == "CTRL+L":
        cursor_x += 1
    elif user_input == "CTRL+M":
        cursor_y += 1
    elif user_input == "CTRL+J":
        cursor_x -= 1
    elif user_input == "CTRL+O":
        cursor_x += 5
    elif user_input == "CTRL+U":
        cursor_x -= 5
    return (cursor_x, cursor_y)

"""
Handle the whole Source Editor
@param "file_vec" : the list obtained from the file (file_to_vec)
@param "cursor_x" : cursor x position
@param "cursor_y" : cursor y position
"""
def main_logic(file_vec, cursor_x, cursor_y):
    # PREPARE TO LAUNCH SOURCE EDITOR
    clear_terminal()

    # MAIN LOOP
    while True:
        # PRINT USER INTERFACE
        print_ui(file_vec, cursor_x, cursor_y)

        # USER KEY GETTER
        try:
            user_input = get_key()
        except:
            user_input = ""
        clear_terminal()

        # USER INPUT HANDLER
        if user_input == "CTRL+W":
            break
        else:
            cursor_tuple = input_handler(user_input, cursor_x, cursor_y)
            cursor_x = cursor_tuple[0]
            cursor_y = cursor_tuple[1]


"""
Start the Source Editor by giving it the path to a specific file
"""
def start_editor(path_to_file):
    # CURSOR POSITION
    cursor_x = 0
    cursor_y = 0
    # TRANSFORM FILE TO A LIST
    file_vec = extend_file_vec(file_to_vec(path_to_file))
    # START MAIN LOGIC
    main_logic(file_vec, cursor_x, cursor_y)
