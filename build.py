import os
import json
import base64
from shutil import copytree, rmtree, move

from settings import *

def generate_resource_pack(resource_dirs, resource_file_name):
    resource_pack = {}
    for resource_dir in resource_dirs:
        for dirpath, dirnames, files in os.walk(resource_dir):
            for file in files:
                filepath = f"{dirpath}/{file}"
                with open(filepath, "rb") as file_data:
                    data = file_data.read()
                    encoded_data = base64.b64encode(data).decode("ascii")
                    resource_pack[filepath] = encoded_data

    with open(WORLD_DATA_PATH, "rb") as file_data:
        data = file_data.read()
        encoded_data = base64.b64encode(data).decode("ascii")
        resource_pack[WORLD_DATA_PATH] = encoded_data


    with open(resource_file_name, 'wb') as save_file:
            save_file.write(base64.b64encode(json.dumps(resource_pack).encode()))



dist_path = f"{os.getcwd()}/dist"

current_directory = f"{os.getcwd()}"

if __name__ == '__main__':

    icon_path = f"res/graphics/icons/icon.ico"

    os.system(f"pyinstaller main.py -n \"{EXECUTABLE_NAME}\" --onefile -i\"{icon_path}\"")

    generate_resource_pack(RESOURCE_DIRS, RESOURCE_FILE_NAME)

    move("bob.res", "dist",)

