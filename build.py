import os
import platform
from shutil import copytree, rmtree, move
from src.utilities.resourcemanager import *

from settings import *

dist_path = f"{os.getcwd()}/dist"

current_directory = f"{os.getcwd()}"

if __name__ == '__main__':

    icon_path = f"res/graphics/icons/icon.ico"

    extension = ""
    
    if platform.system() == 'Windows':
        extension = ".exe"
    if platform.system() == 'Linux':
        extension = ".appimage"
    if platform.system() == 'Darwin':
        extension = ".app"

    os.system(f"pyinstaller --noconsole main.py -n \"{EXECUTABLE_NAME}{extension}\" --onefile -i\"{icon_path}\"")

    generate_resource_pack(RESOURCE_DIRS, RESOURCE_FILE_NAME)

    move("bob.res", "dist",)

