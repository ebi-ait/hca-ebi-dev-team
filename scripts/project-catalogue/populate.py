import argparse, json, os
from ingest.api.ingestapi import IngestApi
from excel.load import SheetLoader

SHEET = "Group 1"
URL = "https://api.ingest.dev.archive.data.humancellatlas.org"
TOKEN = "source/token.txt"

class Populate:
    def __init__(self, file_path, sheet=SHEET, url=URL, token_path=TOKEN):
        self.ingest = IngestApi(url)
        self.token = self.get_token(token_path)
        self.sheet = sheet
        self.path = file_path
        self.loader = SheetLoader(self.path, self.sheet)
    
    def save(self):
        file_path = os.path.splitext(self.path)[0] + ".json"
        output = self.loader.data.as_dict(string_lists=True)
        self.write_dict(file_path, output)

    @staticmethod
    def get_token(token_path):
        with open(token_path, "r") as token_file:
            return token_file.read()
    
    @staticmethod
    def write_dict(file_path: str, data: dict):
        file_path = os.path.abspath(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, "w") as open_file:
            json.dump(data, open_file, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add projects to ingest from datatracker export")
    parser.add_argument('file_path', type=str, help="Excel file exported from datatracker.")
    parser.add_argument("-s", "--sheet", type=str, help="Name of sheet to import", default=SHEET)
    parser.add_argument("-u", "--url", type=str, help="Base URL for Ingest API", default=URL)
    parser.add_argument("-t", "--token_path", type=str, help="Text file containing an ingest token", default=TOKEN)
    args = parser.parse_args()

    populate = Populate(args.file_path, args.sheet, args.url, args.token_path)
    # populate.update_ingest_uuid_from_doi()
    # use dio checker from ingest Ui to ensure that we don't make duplicate projects

    # populate.create_new_ingest_projects()
    # for rows without an ingest uuid
        # map attributes to ingest version using json-converter
        # post new project to ingest
        # save ingest uuid from response
    populate.save()
