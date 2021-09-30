import json


def load_json(filename: str):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data


if __name__ == '__main__':
    submissions_by_project = load_json('summary.json')
    fields = ['biomaterials', 'protocols', 'processes', 'files', 'assays']
    for project, summary in submissions_by_project.items():
        print(f'{project},', end='')
        for field in fields:
            print(summary.get(field), end='')
            print(',', end='')
        print('')

