import json
import os
import logging

def load_ldtk(ldtk_file) -> dict:
    if not os.path.exists(ldtk_file):
        return
    else:
        with open(ldtk_file) as ldtk:
            ldtk_data = json.load(ldtk)
            ldtk_world = LDtkWorldObject()
            ldtk_world.iid = ldtk_data["iid"]
            ldtk_world.table_of_contents = ldtk_data["toc"]
            ldtk_world.world_grid_width = ldtk_data["worldGridWidth"]
            ldtk_world.world_grid_height = ldtk_data["worldGridHeight"]
            ldtk_world.default_level_width = ldtk_data["defaultLevelWidth"]
            ldtk_world.default_level_height = ldtk_data["defaultLevelHeight"]
            ldtk_world.default_grid_size = ldtk_data["defaultGridSize"]
            ldtk_world.default_entity_width = ldtk_data["defaultEntityWidth"]
            ldtk_world.default_entity_height = ldtk_data["defaultEntityHeight"]
            ldtk_world.background_color = ldtk_data["bgColor"]
            ldtk_world.default_background_color = ldtk_data["defaultLevelBgColor"]
            ldtk_world.external_scenes = ldtk_data["externalLevels"]
            ldtk_world.tilesets = ldtk_data["defs"]["tilesets"]
            if not ldtk_world.external_scenes:
                for level in ldtk_data["levels"]:
                    new_scene = load_scene_from_ldtk(level)
                    ldtk_world.scenes.append(new_scene)

            # logging.debug(f"\n {ldtk_world.tilesets} \n")

            return ldtk_world
            
def load_scene_from_ldtk(level):
    new_scene = {}
    new_scene["name"] = level["identifier"]
    new_scene["iid"] = level["iid"]
    new_scene["uid"] = level["uid"]
    new_scene["world_x"] = level["worldX"]
    new_scene["world_y"] = level["worldY"]
    new_scene["width"] = level["pxWid"]
    new_scene["height"] = level["pxHei"]
    new_scene["default_background_color"] = level["__bgColor"]
    new_scene["background_color"] = level["bgColor"]
    new_scene["background_image_path"] = level["bgRelPath"]
    new_scene["background_image_position"] = level["bgPos"]
    new_scene["field_instances"] = level["fieldInstances"]
    new_scene["layer_instances"] = level["layerInstances"]
    new_scene["neighbors"] = level["__neighbours"]
    return new_scene

class LDtkWorldObject:
    def __init__(self) -> None:
        self.iid: str = None
        self.table_of_contents: list = []
        self.world_layout: str = "Gridvania"
        self.world_grid_width: int = 256
        self.world_grid_height: int = 256
        self.default_level_width: int = 256
        self.default_level_height: int = 256
        self.default_grid_size: int = 16
        self.default_entity_width: int = 16
        self.default_entity_height: int = 16
        self.background_color: str = f"000000"
        self.default_background_color: str = f"000000"
        self.external_scenes = False
        self.layers: list = []
        self.entities: list = []
        self.tilesets: list = []
        self.enums: list = []
        self.external_enums: list = []
        self.level_fields: list = []
        self.scenes: list = []
