import pygame

from src.state import State
from src.animatedsprite import AnimatedSprite
from src.screens.gameplay.resources import *

class LoadScene(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.level_name = args[0]
        self.player_start_position = args[1]
        self.transition_in = args[2]

    def on_state_enter(self, level): 
        level.clear_scene()

        for scene in level.game.get_levels_from_world():

            '''here is where the level loading begins'''

            if scene["identifier"] == self.level_name:
                level.width = scene["pxWid"]
                level.height = scene["pxHei"]
                level.bg_color = scene["__bgColor"]
                for level_property in scene["fieldInstances"]:
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
                
                for layer in scene["layerInstances"]:
                    if layer["__identifier"] == GROUND_2_LAYER_NAME:
                        level.ground_2["tileset"] = layer["__tilesetRelPath"]
                        level.ground_2["grid_size"] = layer["__gridSize"]
                        level.ground_2["tiles"] = layer["gridTiles"]
                        level.game.load_tileset(f"{BASE_PATH}{level.ground_2['tileset']}", level.tilesets)

                    if layer["__identifier"] == MAIN_GROUND_LAYER_NAME:
                        level.main_ground["tileset"] = layer["__tilesetRelPath"]
                        level.main_ground["grid_size"] = layer["__gridSize"]
                        level.main_ground["tiles"] = layer["autoLayerTiles"]
                        level.game.load_tileset(f"{BASE_PATH}{level.main_ground['tileset']}", level.tilesets)


                level.camera.set_bounds(0, level.width, 0, level.height)
                level.camera.center(self.player_start_position[0], self.player_start_position[1])



        if self.transition_in == "money_in":
            level.money_in_transition()