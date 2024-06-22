from settings import *
import base64
import json


with open(SAVE_DATA_FILE_NAME) as save_file_database:
    save_file_database_decoded = base64.b64decode(save_file_database.read())
    save_file_database_data = json.loads(save_file_database_decoded)

    print(save_file_database_data)