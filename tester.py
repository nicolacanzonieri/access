# TESTER

from utils.dir_util import get_path_to
from utils.json_util import *
from utils.str_util import clean_str

def test_json_util():
    path_to_json = get_path_to("json template.json")
    print_json_vec(path_to_json)

def test_str_util():
    string = "   Mario Rossi"
    print(clean_str(string))

def main():
    test_json_util()

main()