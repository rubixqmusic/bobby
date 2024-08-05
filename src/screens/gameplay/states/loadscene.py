import pygame
from math import floor
import json

from src.state import State
from src.animatedsprite import AnimatedSprite
from src.screens.gameplay.resources import *
from src.entities.bobby.bobby import Bobby
from src.components.hitbox import Hitbox

class LoadScene(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.scene_name = args[0]
        self.player_start_position = args[1]
        self.transition_in = args[2]

    def on_state_enter(self, level): 
        self.game = level.game
        level.clear_scene()

        for scene in level.game.get_levels_from_world():

            '''here is where the level loading begins'''

            if scene["identifier"] == self.scene_name:
                level.width = scene["pxWid"]
                level.height = scene["pxHei"]
                level.bg_color = scene["__bgColor"]
                for level_property in scene["fieldInstances"]:
                    if level_property["__identifier"] == "gravity":
                        level.gravity = level_property["__value"]
                    if level_property["__identifier"] == "music":
                        if level_property["__value"] in LEVEL_MUSIC:
                            level.game.play_music(LEVEL_MUSIC[level_property["__value"]])
                    if level_property["__identifier"] == "animated_background":
                        if level_property["__value"]:
                            background_data = json.loads(level_property["__value"])

                            if "image" in background_data and "animation" in background_data:

                                bg_image_path = f"{GRAPHICS_PATH}/animated_backgrounds/{background_data['image']}{BACKGROUND_IMAGE_FILE_EXTENSION}"
                                bg_animation_data = f"{ANIMATIONS_PATH}/{background_data['animation']}.json"
                                
                                if level.game.resource_exists(bg_image_path) and level.game.resource_exists(bg_animation_data):
                                    level.bg_image = AnimatedSprite(level.game, level.camera.surface)
                                    level.bg_image.load_spritesheet(bg_image_path)
                                    level.bg_image.load_sprite_data(bg_animation_data)
                                    level.bg_image.set_animation("idle")
                                    level.bg_image.set_position(0,0)
                                    level.bg_image.play()
                    
                    if level_property["__identifier"] == "background_1":
                        if level_property["__value"]:
                            background_data = json.loads(level_property["__value"])
                            if "image" in background_data:
                                bg_image_path = f"{GRAPHICS_PATH}/scene_backgrounds/{background_data['image']}{BACKGROUND_IMAGE_FILE_EXTENSION}"
                                
                                if level.game.resource_exists(bg_image_path):
                                    level.bg_1 = {}
                                    level.bg_1["parallax_x"] = 0.01
                                    level.bg_1["parallax_y"] = 0.0
                                    level.bg_1["image"] = pygame.image.load(level.game.load_resource(bg_image_path))
                            
                    if level_property["__identifier"] == "background_2":
                        if level_property["__value"]:
                            background_data = json.loads(level_property["__value"])
                            if "image" in background_data:
                                bg_image_path = f"{GRAPHICS_PATH}/scene_backgrounds/{background_data['image']}{BACKGROUND_IMAGE_FILE_EXTENSION}"
                                
                                if level.game.resource_exists(bg_image_path):
                                    level.bg_2 = {}
                                    level.bg_2["parallax_x"] = 0.05
                                    level.bg_2["parallax_y"] = 0.0
                                    level.bg_2["image"] = pygame.image.load(level.game.load_resource(bg_image_path))

                    if level_property["__identifier"] == "background_3":
                        if level_property["__value"]:
                            background_data = json.loads(level_property["__value"])
                            if "image" in background_data:
                                bg_image_path = f"{GRAPHICS_PATH}/scene_backgrounds/{background_data['image']}{BACKGROUND_IMAGE_FILE_EXTENSION}"
                                
                                if level.game.resource_exists(bg_image_path):
                                    level.bg_3 = {}
                                    level.bg_3["parallax_x"] = 0.1
                                    level.bg_3["parallax_y"] = 0.0
                                    level.bg_3["image"] = pygame.image.load(level.game.load_resource(bg_image_path))
                
                tileset_data = self.get_tileset_data()

                for layer in scene["layerInstances"]:
                    if layer["__identifier"] == GROUND_2_LAYER_NAME:
                        level.ground_2["tileset"] = layer["__tilesetRelPath"]
                        level.ground_2["grid_size"] = layer["__gridSize"]
                        level.ground_2["tiles"] = layer["gridTiles"]
                        level.game.load_tileset(f"{BASE_PATH}{level.ground_2['tileset']}", level.tilesets)

                        if tileset_data:
                            for tile in level.ground_2["tiles"]:
                                tile_id = self.get_tile_id_from_x_y(tile["src"][0], tile["src"][1], tileset_data["width"], level.ground_2["grid_size"])                                
                                if tile_id in tileset_data:
                                    tile_type = tileset_data[tile_id]
                                    hitbox = Hitbox()
                                    hitbox.set_type(tile_type)
                                    hitbox.set_hitbox(tile["px"][0], tile["px"][1], level.ground_2["grid_size"], level.ground_2["grid_size"])
                                    hitbox.set_position(tile["px"][0], tile["px"][1])
            
                                    level.register_hitbox(hitbox)

                    if layer["__identifier"] == MAIN_GROUND_LAYER_NAME:
                        level.main_ground["tileset"] = layer["__tilesetRelPath"]
                        level.main_ground["grid_size"] = layer["__gridSize"]
                        level.main_ground["tiles"] = layer["autoLayerTiles"]
                        level.game.load_tileset(f"{BASE_PATH}{level.main_ground['tileset']}", level.tilesets)

                        if tileset_data:
                            for tile in level.main_ground["tiles"]:
                                tile_id = self.get_tile_id_from_x_y(tile["src"][0], tile["src"][1], tileset_data["width"], level.main_ground["grid_size"])
                                if tile_id in tileset_data:
                                    tile_type = tileset_data[tile_id]
                                    hitbox = Hitbox()
                                    hitbox.set_type(tile_type)
                                    hitbox.set_hitbox(tile["px"][0], tile["px"][1], level.main_ground["grid_size"], level.main_ground["grid_size"])
                                    hitbox.set_position(tile["px"][0], tile["px"][1])
                                    level.register_hitbox(hitbox)

                    if layer["__identifier"] == ENTITIES_LAYER_NAME:
                        entity_instances = layer["entityInstances"]
                        for entity in entity_instances:
                            new_entity = level.spawn_new_entity(entity)
                            if new_entity:
                                if new_entity.has_method("set_position"):
                                    new_entity.set_position(entity["px"][0], entity["px"][1])
                                level.add_entity_to_scene(new_entity)
                            # if entity["__identifier"] == GOLD_COIN_ENTITY:
                            #     new_coin = Coin(entity["px"], level.camera, DEFAULT_GRAVITY, level.camera.surface, level.hitboxes, GOLD_COIN_ENTITY)
                            #     level.register_hitbox(new_coin.hitbox)
                            #     level.entities.append(new_coin)

                level.camera.set_bounds(0, level.width, 0, level.height)
                level.camera.center(self.player_start_position[0], self.player_start_position[1])
                level.player = Bobby(level)
                level.player.set_position(self.player_start_position[0], self.player_start_position[1])
                # level.player.generate_particles.attach(level.particle_engine, "generate_particles")

        level._add_queued_entities_to_scene()

        if self.transition_in == "money_in":
            level.money_in_transition()
    
    def get_tileset_data(self):
        tileset_data = {}
        world = self.game.get_world()
        if world:
            tilesets = world["defs"]["tilesets"]

            for tileset in tilesets:
                if tileset["identifier"] == LEVEL_TILESET_IDENTIFIER:

                    tileset_data['width'] = tileset["pxWid"]/tileset["tileGridSize"]
                    
                    for data in tileset["customData"]:
                        if data["data"] in TILE_HITBOX_TYPES:
                            tileset_data[data["tileId"]] = TILE_HITBOX_TYPES[data["data"]]
            # print(tileset_data)
        return tileset_data
    
    def get_tile_id_from_x_y(self, x, y, tileset_width_in_tiles, grid_size):
        x = floor(x/grid_size)
        y = floor(y/grid_size)


        return int(y * tileset_width_in_tiles + x)
    


