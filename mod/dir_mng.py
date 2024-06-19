'''
DIRECTORY MANAGER

This code contains functions that are used to initialize and verify that all the files that ACCESS needs exists


Index:
- initialize_directory()

'''


import os
from utils.dir_util import get_path_to, get_prnt_folder, check, create_file

current_path = get_path_to(os.getcwd() + " mod dir_mng.py")


'''
Check and initialize `source.txt` and database' files
'''
def initialize_directory():
    source_path = get_prnt_folder(current_path, 2) + get_path_to("source.txt")

    if not check(source_path):
        print("Initializing source")
        create_file(source_path, "")