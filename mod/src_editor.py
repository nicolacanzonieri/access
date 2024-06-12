"""
SOURCE EDITOR

This code contains functions that allows user to modify the ACCESS source without leaving the software
"""

import threading
import sys
import os


from enum import Enum

from utils.dir_util import get_path_to
from utils.file_util import get_file
from utils.vec_util import print_matrix


class Mode(Enum):
    NAVIGATION = 0
    EDIT = 1


mode = Mode.NAVIGATION
cursor_x = 0
cursor_y = 0


if sys.platform == "win32":
    import msvcrt

    def get_key():
        while True:
            key = msvcrt.getch()
            if key == b"\x0D":  # Ctrl+M (Enter key)
                return "CTRL+M"
            elif key == b'\x11':  # Ctrl+Q
                return 'CTRL+Q'
            elif key == b'\x08':  # Backspace/Delete key
                return 'DELETE'
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
            if ord(key) == 13:  # Ctrl+M (Enter key)
                return "CTRL+M"
            elif ord(key) == 17:  # Ctrl+Q
                return 'CTRL+Q'
            elif ord(key) == 127:  # Backspace/Delete key
                return 'DELETE'
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def print_editor(file_vec, mode):
    line_x_index = 0

    print("[ CTRL-M : Change mode ] [ CTRL-Q : Close Editor ] [ SHIFT-A/SHIFT-D: Move faster ]\n")
    print("MODE: " + mode.name) 
    print("\n\n\n", end="")

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
        elif user_input == "CTRL+M":
            if mode == Mode.NAVIGATION:
                mode = Mode.EDIT
            else:
                mode = Mode.NAVIGATION
        elif user_input == "w" and mode == Mode.NAVIGATION:
            cursor_y -= 1
            if cursor_y < 0:
                cursor_y = 0
        elif user_input == "a" and mode == Mode.NAVIGATION:
            cursor_x -= 1
            if cursor_x < 0:
                cursor_x = 0
        elif user_input == 'A' and mode == Mode.NAVIGATION:
            cursor_x -= 5
            if cursor_x < 0:
                cursor_x = 0
        elif user_input == "s" and mode == Mode.NAVIGATION:
            cursor_y += 1
        elif user_input == "d" and mode == Mode.NAVIGATION:
            cursor_x += 1
        elif user_input == 'D' and mode == Mode.NAVIGATION:
            cursor_x += 5
        elif user_input == "DELETE" and mode == Mode.EDIT:
            print()
            # TODO: Add a way to modify the values of the file


def start(file_vec):
    main_logic_thread = threading.Thread(main_logic(file_vec))

    main_logic_thread.start()

    # Wait for both threads to finish before exiting
    main_logic_thread.join()


def test(path_to_file):
    file_vec = file_to_vec(path_to_file)
    start(file_vec)
