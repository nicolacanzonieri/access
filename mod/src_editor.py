"""
SOURCE EDITOR

This code contains a simple text editor that will be used to edit source file directly inside ACCESS, so user
don't need to leave the software.


Index:
- get_key()
- edit_file()
- clear_terminal()
- mng_input()
- print_editor()
- main_logic()
- start_src_editor()

"""

import threading
import sys
import os


from enum import Enum

from utils.file_util import file_to_vec
from utils.dir_util import get_path_to
from utils.json_util import get_json_value
from utils.var_util import string_to_int
from utils.str_util import clean_str


'''
Enum containing the possible modes that the user need while editing the file
'''
class Mode(Enum):
    NAVIGATION = 0
    EDIT = 1


'''
Global variables
'''
mode = Mode.NAVIGATION
cursor_x = 0
cursor_y = 0
last_key = ""
max_string_length = string_to_int(get_json_value(get_path_to("json sys_var.json"), 0))


'''
Detect special keys pressed by the user
'''
if sys.platform == "win32":
    import msvcrt

    def get_key():
        while True:
            key = msvcrt.getch()
            if key == b"\x0D":  # Ctrl+M (Enter key)
                return "CTRL+M"
            elif key == b"\x11":  # Ctrl+Q
                return "CTRL+Q"
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
            if ord(key) == 13:
                return "CTRL+M"
            elif ord(key) == 17:
                return "CTRL+Q"
            elif ord(key) == 127:
                return "DELETE"
            elif ord(key) == 126:
                return "CANCEL"
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key


'''
Return the updated file_vec after editing it
@param "file_vec" : list containing the file
@param "user_input" : string containing the key that the user pressed
@param "cursor_x" : current x position of the cursor
@param "cursor_y" : current y position of the cursor
'''
def edit_file(file_vec, user_input, cursor_x, cursor_y) -> list:
    global last_key

    if user_input == "DELETE":
        if cursor_x > 0:
            file_vec[cursor_y] = (
                file_vec[cursor_y][: cursor_x - 1] + file_vec[cursor_y][cursor_x:]
            )
            last_key = user_input
            return [file_vec, cursor_x - 1]
        else:
            return [file_vec, cursor_x]
    elif user_input == "CANCEL":
        file_vec[cursor_y] = (
            file_vec[cursor_y][:cursor_x] + file_vec[cursor_y][cursor_x + 1 :]
        )
        last_key = user_input
        return [file_vec, cursor_x - 1]
    else:
        if last_key != "CANCEL":
            file_vec[cursor_y] = (
                file_vec[cursor_y][: cursor_x + 1]
                + user_input
                + file_vec[cursor_y][cursor_x + 1 :]
            )
            last_key = user_input
            return [file_vec, cursor_x + 1]
        else:
            return [file_vec, cursor_x + 1]


'''
Clear terminal
'''
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


'''
Return the updated file_vec after detecting user input.
Note that this function calls "edit_file" function
@param "file_vec" : list containing the file
@param "user_input" : string containing the key that the user pressed
@param "cursor_x" : current x position of the cursor
@param "cursor_y" : current y position of the cursor
'''
def mng_input(file_vec, user_input, mode, cursor_x, cursor_y) -> list:
    if user_input == "CTRL+M":
        if mode == Mode.NAVIGATION:
            mode = Mode.EDIT
        else:
            mode = Mode.NAVIGATION
    elif user_input == "w" and mode == Mode.NAVIGATION:
        cursor_y -= 1

        try:
            if len(file_vec[cursor_y]) < cursor_x:
                cursor_x = len(file_vec[cursor_y]) - 1
                if cursor_x < 0:
                    cursor_x = 0
        except:
            None

        if cursor_y < 0:
            cursor_y = 0
    elif user_input == "a" and mode == Mode.NAVIGATION:
        cursor_x -= 1
        if cursor_x < 0:
            cursor_x = 0
    elif user_input == "A" and mode == Mode.NAVIGATION:
        cursor_x -= 5
        if cursor_x < 0:
            cursor_x = 0
    elif user_input == "s" and mode == Mode.NAVIGATION:
        cursor_y += 1

        try:
            if len(file_vec[cursor_y]) < cursor_x:
                cursor_x = len(file_vec[cursor_y]) - 1
                if cursor_x < 0:
                    cursor_x = 0
        except:
            None

        if cursor_y > len(file_vec):
            cursor_y = len(file_vec)
    elif user_input == "d" and mode == Mode.NAVIGATION:
        cursor_x += 1
        if cursor_x >= len(file_vec[cursor_y]):
            cursor_x = len(file_vec[cursor_y]) - 1
    elif user_input == "D" and mode == Mode.NAVIGATION:
        cursor_x += 5
        if cursor_x >= len(file_vec[cursor_y]):
            cursor_x = len(file_vec[cursor_y]) - 1
    elif mode == Mode.EDIT:
        handler = edit_file(file_vec, user_input, cursor_x, cursor_y)
        file_vec = handler[0]
        cursor_x = handler[1]
    return [file_vec, user_input, mode, cursor_x, cursor_y]


'''
Print the editor visualization
@param "file_vec" : list containing the file
@param "mode" : Mode that represent current user mode
'''
def print_editor(file_vec, mode):
    line_x_index = 0

    print(
        "[ CTRL-M : Change mode ] [ CTRL-Q : Close Editor ] [ SHIFT-A/SHIFT-D: Move faster ]\n"
    )
    print("MODE: " + mode.name)
    print("\n\n\n", end="")

    fixed_file_vec = []
    for line_y_index, line in enumerate(file_vec):
        if len(line) > max_string_length:
            fixed_file_vec.append(line[ : max_string_length])
            fixed_file_vec.append(clean_str(line[max_string_length : ]))
        else:
            fixed_file_vec.append(file_vec[line_y_index])
    file_vec = fixed_file_vec
        
    for line_y_index, line in enumerate(file_vec):
        print(line)
        blank_line_index = 0
        while blank_line_index < len(line):
            # If we are in the cursor position, draw it
            if cursor_x == line_x_index and cursor_y == line_y_index:
                print("^", end="")
            else:
                print(" ", end="")
            line_x_index += 1
            blank_line_index += 1
        line_x_index = 0
        print()


'''
Main logic of the software
@param "file_vec" : list containing the file
'''
def main_logic(file_vec):
    global mode
    global cursor_x
    global cursor_y

    clear_terminal()
    while True:
        print_editor(file_vec, mode)
        try:
            user_input = get_key()
        except:
            user_input = ""
        clear_terminal()

        if user_input == "CTRL+Q":
            break
        else:
            handler = mng_input(file_vec, user_input, mode, cursor_x, cursor_y)
            file_vec = handler[0]
            user_input = handler[1]
            mode = handler[2]
            cursor_x = handler[3]
            cursor_y = handler[4]


def start_src_editor(path_to_file):
    file_vec = file_to_vec(path_to_file)
    main_logic_thread = threading.Thread(main_logic(file_vec))

    main_logic_thread.start()

    main_logic_thread.join()
