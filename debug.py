'''
DEBUG

'''

from utils.dir_util import get_path_to
from utils.json_util import json_reader

def test_json_reader():
    path_to_json = get_path_to("json example.json")
    json_reader(path_to_json)

def main():
    test_json_reader()

main()