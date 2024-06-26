import os
import json
import base64
from shutil import copytree, rmtree, move
from src.utilities.resourcemanager import *

from settings import *

dist_path = f"{os.getcwd()}/dist"

current_directory = f"{os.getcwd()}"

if __name__ == '__main__':

    icon_path = f"res/graphics/icons/icon.ico"

    os.system(f"pyinstaller --noconsole main.py -n \"{EXECUTABLE_NAME}\" --onefile -i\"{icon_path}\"")

    generate_resource_pack(RESOURCE_DIRS, RESOURCE_FILE_NAME)

    move("bob.res", "dist",)

