import json


def load_json(filename: str):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data


def write_json(data: dict, filename: str):
    with open(filename, "w") as open_file:
        json.dump(data, open_file, indent=2)