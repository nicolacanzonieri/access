'''
SOURCE EDITOR


Index:
- get_key()
- clear_terminal()
- print_ui()
- main_logic()
- start()
'''


import sys
import os

from utils.file_util import file_to_vec
from utils.json_util import get_json_value
from utils.dir_util import get_path_to
from utils.var_util import str_to_int


'''
SYSTEM VARIABLES
'''
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
            if key == b"\x11":  # Ctrl+Q
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
            if ord(key) == 17:
                return "CTRL+Q"
            elif ord(key) == 127:
                return "DELETE"
            elif ord(key) == 126:
                return "CANCEL"
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key


'''
Clear terminal
'''
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


'''
Print a text line that is longer than ‘max_string_length‘
@param "file_line" : the interested text_line
'''
def print_long_line(file_line):
    repeater = len(file_line)/max_string_length
    repeater_index = 0
    while repeater_index < repeater:
        if repeater_index == 0:
            print(file_line[ : max_string_length])
        elif repeater_index == repeater - 1:
            start_point = repeater_index * max_string_length
            print(file_line[start_point : ])
        else:
            start_point = repeater_index * max_string_length
            end_point = start_point + max_string_length
            print(file_line[start_point : end_point])
        print("")
        repeater_index += 1


'''
Print UI
@param "file_vec" : the list obtained from the file (file_to_vec)
'''
def print_ui(file_vec):
	file_vec_len = len(file_vec)
	file_vec_index = 0
	
	# PRINTER
	while file_vec_index < file_vec_len:
		file_line = file_vec[file_vec_index]
        # IF LINE IS LONGER THAN THE MAX STRING LENGTH VARIABLE
		if len(file_line) > max_string_length:
			print_long_line(file_line)
		else:
			print(file_line)
			print("")
		file_vec_index += 1


'''
Handle the whole Source Editor
@param "file_vec" : the list obtained from the file (file_to_vec)
'''
def main_logic(file_vec):
	# PREPARE TO LAUNCH SOURCE EDITOR
	clear_terminal()
	
	# MAIN LOOP
	while True:
        # PRINT USER INTERFACE
		print_ui(file_vec)
		
		# USER KEY GETTER
		try:
			user_input = get_key()
		except:
			user_input = ""
		
		clear_terminal()
		
		# USER INPUT HANDLER
		if user_input == "CTRL+Q":
			break


'''
Start the Source Editor by giving it the path to a specific file
'''
def start(path_to_file):
    # TRANSFORM FILE TO A LIST
    file_vec = file_to_vec(path_to_file)
	# START MAIN LOGIC
    main_logic(file_vec)