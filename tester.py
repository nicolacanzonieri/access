'''
TESTER
'''

from mod.src_editor import start_src_editor
from utils.dir_util import get_path_to
from utils.json_util import print_json_vec
from utils.str_util import clean_str


# SOURCE EDITOR TESTER
def test_src_editor():
    path_to_src = get_path_to("source.txt")
    start_src_editor(path_to_src)


# JSON UTILS TESTER
def test_json_util():
    path_to_json = get_path_to("json template.json")
    print_json_vec(path_to_json)


# STR UTILS TESTER
def test_str_util():
    string = "   Mario Rossi"
    print(clean_str(string))


# MAIN
def main():
    test_src_editor()

main()