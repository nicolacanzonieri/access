"""
SYSTEM VARIABLES INITIALIZATION

This code is executed at the very start when launching ACCESS. Its purpose is to initialize variables that
the codes need


Index:
- get_key()
- clear_terminal()
- get_max_string_length_thread()
- init_max_string_length()

"""

import threading
import sys
import os


from utils.json_util import edit_json


'''
Value of the max string length choosed by the user
'''
max_string_length = 0


'''
Detect special keys pressed by the user
'''
if sys.platform == "win32":
    import msvcrt

    def get_key():
        while True:
            key = msvcrt.getch()
            if key == b"\x0D":  # Ctrl+M (Enter key)
                return "ENTER"
            if key == b'\x1b':
                return "ESCAPE"
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
                return "ENTER"
            if ord(key) == 27:
                return "ESCAPE"
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key


'''
Clear terminal
'''
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


'''
Function started by a thread in get_max_string_length
'''
def get_max_string_length_thread():
    global max_string_length
    length_vis = "##########"
    clear_terminal()

    while True:
        print(
            "Press 'A' or 'D' to adjust the length of the string according to your window width"
        )
        print("Press 'SHIFT+A' or 'SHIFT+D' to quick increase the length value")
        print("")
        print(length_vis)
        print("\n")
        print("Press ENTER to finish or press ESC to exit without saving")
        try:
            user_input = get_key()
        except:
            user_input = ""
        clear_terminal()

        if user_input == "ENTER":
            max_string_length = len(length_vis)
            break
        elif user_input == "ESCAPE":
            break
        elif user_input == "a":
            length_vis = length_vis[: len(length_vis) - 1]
        elif user_input == "d":
            length_vis += "#"
        elif user_input == "A":
            try:
                length_vis = length_vis[: len(length_vis) - 5]
            except:
                length_vis = ""
        elif user_input == "D":
            length_vis += "#####"


'''
Return the preferred max string length choosed by the user 
'''
def init_max_string_length(path_to_json):
    get_max_string_length = threading.Thread(get_max_string_length_thread())

    get_max_string_length.start()

    # Wait for both threads to finish before exiting
    get_max_string_length.join()

    if max_string_length != 0:
        edit_json(path_to_json, 1, '"' + str(max_string_length) + '"')