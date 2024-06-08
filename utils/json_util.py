def json_reader(path_to_json):
    with open(path_to_json, "r") as file:
        text = file.read()
        print(text)