import re

# ToDo: Move this to json-converter
def fixed_attribute(*args):
    value = args[1]
    return value

def map_value(*args):
    key = args[0]
    map = args[1]
    if isinstance(map, dict):
        return map.get(key, '')

def removeHTMLTags(*args):
    regex = re.compile(r'<([^>]+)>')
    input = args[0]
    if isinstance(input, str):
        return regex.sub('', input)

def first_map(*args):
    array = args[0]
    key = args[1]
    if isinstance(array, list) and len(array) > 0 and isinstance(array[0], dict):
        return array[0].get(key, None)

def append(*args):
    input = args[0]
    post_script = args[1]
    if input and post_script:
        return input + post_script
