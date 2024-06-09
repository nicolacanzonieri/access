'''
SOURCE EDITOR

This code contains functions that allows user to modify the ACCESS source without leaving the software
'''


'''
Start source editor
@param "path_to_src" : a string containing the path to `source.txt`
'''
def start_src_editor(path_to_src):
    with open(path_to_src, "r+") as src_file:
        src = src_file.read()
        print(src)
    print("")
    # TODO!