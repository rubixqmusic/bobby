import os
import json
import base64

def generate_resource_pack():
    resource_pack = {}

    resource_dirs = ["res/animations", 
                    "res/audio/fx", 
                    "res/audio/music", 
                    "res/fonts", 
                    "res/graphics/animated_tilesets", 
                    "res/graphics/backgrounds",
                    "res/graphics/entities", 
                    "res/graphics/hud", 
                    "res/graphics/icons",
                    "res/graphics/player",
                    "res/graphics/scene_backgrounds",
                    "res/graphics/scene_backgrounds/bg_1",
                    "res/graphics/scene_backgrounds/bg_2",
                    "res/graphics/scene_backgrounds/bg_3",
                    "res/graphics/scene_backgrounds/bg_image",
                    "res/graphics/screen_transitions",
                    "res/graphics/text_box",
                    "res/graphics/tilesets",
                    "res/graphics/video_call_cutscenes",
                    "res/graphics/world_map",
                    "res/tileset_animations"
                    ]
    for resource_dir in resource_dirs:
        for dirpath, dirnames, files in os.walk(resource_dir):
            for file in files:
                filepath = f"{dirpath}/{file}"
                # print(f"{dirpath}{file}")
                with open(filepath, "rb") as file_data:
                    data = file_data.read()
                    encoded_data = base64.b64encode(data).decode("ascii")
                    resource_pack[filepath] = encoded_data

    with open("res/bobby.ldtk", "rb") as file_data:
        data = file_data.read()
        encoded_data = base64.b64encode(data).decode("ascii")
        resource_pack["res/bobby.ldtk"] = encoded_data


    with open("bob.res", 'wb') as save_file:
            save_file.write(base64.b64encode(json.dumps(resource_pack).encode()))
        
        # json.dump(resource_pack, save_file)


            