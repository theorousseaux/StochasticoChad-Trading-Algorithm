import json


def ReadJSON(path):
    with open(path) as f:
        return json.load(f)
