"""
SOURCE EDITOR


Index:
- get_key()
- clear_terminal()
- print_cursor()
- print_long_line()
- print_ui()
- main_logic()
- start()
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


"""
Print the cursor line with the cursor
@param "line" : the string that we are modifying
@param "cursor_x" : the cursor x position
"""
def print_cursor(line, cursor_x):
    line_index = 0
    while line_index <= len(line):
        if line_index == cursor_x:
            print("^")
        else:
            print(" ")
        line_index += 1


"""
Print a text line that is longer than ‘max_string_length‘
@param "file_line" : the interested text_line
@param "cursor_line" : true if function have to print cursor line, false if not
@param "cursor_x" : cursor x position
"""
def print_long_line(file_line, is_cursor_line, cursor_x):
    repeater = int(len(file_line) / max_string_length)
    cursor_repeater = int(cursor_x / max_string_length) - 1
    repeater_index = 0
    while repeater_index < repeater:
        if repeater_index == 0:
            temp_line = file_line[:max_string_length]
            print(temp_line)
        elif repeater_index == repeater - 1:
            start_point = repeater_index * max_string_length
            temp_line = file_line[start_point:]
            print(temp_line)
        else:
            start_point = repeater_index * max_string_length
            end_point = start_point + max_string_length
            temp_line = file_line[start_point:end_point]
            print(temp_line)
        if repeater_index == cursor_repeater:
            print_cursor(temp_line, cursor_x)
        repeater_index += 1


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

        # IF LINE IS LONGER THAN THE MAX STRING LENGTH VARIABLE
        if len(file_line) > max_string_length:
            print_long_line(file_line, is_cursor_line, cursor_x)
        else:
            print(file_line)
            if is_cursor_line:
                print_cursor(file_line, cursor_x)
        file_vec_index += 1


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


"""
Start the Source Editor by giving it the path to a specific file
"""
def start(path_to_file):
    # CURSOR POSITION
    cursor_x = 0
    cursor_y = 0
    # TRANSFORM FILE TO A LIST
    file_vec = file_to_vec(path_to_file)
    # START MAIN LOGIC
    main_logic(file_vec, cursor_x, cursor_y)
