import os
from shutil import copytree, rmtree, move
from res.settings import *
from resource_packer import generate_resource_pack


# icon_path = f"{os.getcwd()}/graphics/icons/icon.ico"

dist_path = f"{os.getcwd()}/dist"

current_directory = f"{os.getcwd()}"

# bundle_prefix = BUNDLE_PREFIX

# dist_path = f"{dist_path}/{bundle_prefix}"

if __name__ == '__main__':

    # dist_path = f"{dist_path}/{bundle_prefix}"
    icon_path = f"res/graphics/icons/icon.ico"

    os.system(f"pyinstaller main.py -n \"{EXECUTABLE_NAME}\" --onefile -i\"{icon_path}\"")

    generate_resource_pack()

    move("bob.res", "dist",)

    # copytree(f"{current_directory}/animations", f"{dist_path}animations")
    # copytree(f"{current_directory}/audio", f"{dist_path}audio")
    # copytree(f"{current_directory}/fonts", f"{dist_path}fonts")
    # copytree(f"{current_directory}/hud", f"{dist_path}hud")
    # copytree(f"{current_directory}/graphics", f"{dist_path}graphics")
    # copytree(f"{current_directory}/scenes", f"{dist_path}scenes")
    # copytree(f"{current_directory}/templates", f"{dist_path}templates")
    # copytree(f"{current_directory}/tilesets", f"{dist_path}tilesets")
    # copytree(f"{current_directory}/utilities", f"{dist_path}utilities")
    # copytree(f"{current_directory}/worlds", f"{dist_path}worlds")

    # rmtree(f"{dist_path}graphics/projectfiles")
