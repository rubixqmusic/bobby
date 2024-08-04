import os
import platform
from shutil import copytree, rmtree, move
from src.utilities.resourcemanager import *

from settings import *

dist_path = f"{os.getcwd()}/dist"
build_path = f"{os.getcwd()}/build"

current_directory = f"{os.getcwd()}"

if __name__ == '__main__':

    os.environ["ENV"] = PRODUCTION_ENVIRONMENT_VARIABLE

    icon_path = f"res/graphics/icons/icon.ico"

    extension = ""
    
    if platform.system() == 'Windows':
        extension = ".exe"
    if platform.system() == 'Linux':
        extension = ".appimage"
    if platform.system() == 'Darwin':
        extension = ".app"

    if os.path.exists(dist_path):
        rmtree(dist_path)
    if os.path.exists(build_path):
        rmtree(build_path)

    os.system(f"pyinstaller --noconsole main.py -n \"{EXECUTABLE_NAME}{extension}\" --onefile -i\"{icon_path}\"")

    generate_resource_pack(RESOURCE_DIRS, RESOURCE_FILE_NAME)

    move("bob.res", "dist",)

    # os.environ["ENV"] = DEVELOPMENT_ENVIRONMENT_VARIABLE

