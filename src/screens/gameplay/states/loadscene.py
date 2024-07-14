import pygame
from math import floor

from src.state import State
from src.animatedsprite import AnimatedSprite
from src.screens.gameplay.resources import *
from src.entities.bobby.bobby import Bobby
from src.components.hitbox import Hitbox

class LoadScene(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.level_name = args[0]
        self.player_start_position = args[1]
        self.transition_in = args[2]

    def on_state_enter(self, level): 
        self.game = level.game
        level.clear_scene()

        for scene in level.game.get_levels_from_world():

            '''here is where the level loading begins'''

            if scene["identifier"] == self.level_name:
                level.width = scene["pxWid"]
                level.height = scene["pxHei"]
                level.bg_color = scene["__bgColor"]
                for level_property in scene["fieldInstances"]:
                    if level_property["__identifier"] == "gravity":
                        level.gravity = level_property["__value"]
                    if level_property["__identifier"] == "music":
                        if level_property["__value"] in LEVEL_MUSIC:
                            level.game.play_music(LEVEL_MUSIC[level_property["__value"]])
                    if level_property["__identifier"] == "background":
                        if level_property["__value"]:
                            bg_image_path = f"{GRAPHICS_PATH}/scene_backgrounds/bg_image/{level_property['__value']}{BACKGROUND_IMAGE_FILE_EXTENSION}"
                            bg_animation_data = f"{ANIMATIONS_PATH}/{level_property['__value']}.json"
                            
                            if level.game.resource_exists(bg_image_path) and level.game.resource_exists(bg_animation_data):
                                level.bg_image = AnimatedSprite(level.game, level.camera.surface)
                                level.bg_image.load_spritesheet(bg_image_path)
                                level.bg_image.load_sprite_data(bg_animation_data)
                                level.bg_image.set_animation("idle")
                                level.bg_image.set_position(0,0)
                                level.bg_image.play()
                            
                            bg_image_path = f"{GRAPHICS_PATH}/scene_backgrounds/bg_1/{level_property['__value']}{BACKGROUND_IMAGE_FILE_EXTENSION}"
                            
                            if level.game.resource_exists(bg_image_path):
                                level.bg_1 = {}
                                level.bg_1["parallax_x"] = 0.01
                                level.bg_1["parallax_y"] = 1.0
                                level.bg_1["image"] = pygame.image.load(level.game.load_resource(bg_image_path))
                            
                            bg_image_path = f"{GRAPHICS_PATH}/scene_backgrounds/bg_2/{level_property['__value']}{BACKGROUND_IMAGE_FILE_EXTENSION}"
                            
                            if level.game.resource_exists(bg_image_path):
                                level.bg_2 = {}
                                level.bg_2["parallax_x"] = 0.05
                                level.bg_2["parallax_y"] = 0.9
                                level.bg_2["image"] = pygame.image.load(level.game.load_resource(bg_image_path))

                            bg_image_path = f"{GRAPHICS_PATH}/scene_backgrounds/bg_3/{level_property['__value']}{BACKGROUND_IMAGE_FILE_EXTENSION}"
                            
                            if level.game.resource_exists(bg_image_path):
                                level.bg_3 = {}
                                level.bg_3["parallax_x"] = 0.6
                                level.bg_3["parallax_y"] = 0.3
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

                


                level.camera.set_bounds(0, level.width, 0, level.height)
                level.camera.center(self.player_start_position[0], self.player_start_position[1])
                level.player = Bobby([self.player_start_position[0], self.player_start_position[1]], level.camera, DEFAULT_GRAVITY, level.camera.surface, level.hitboxes)

        # print(level.hitboxes)

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

                        tileset_data[data["tileId"]] = data["data"]
            # print(tileset_data)
        return tileset_data
    
    def get_tile_id_from_x_y(self, x, y, tileset_width_in_tiles, grid_size):
        x = floor(x/grid_size)
        y = floor(y/grid_size)


        return int(y * tileset_width_in_tiles + x)
    


