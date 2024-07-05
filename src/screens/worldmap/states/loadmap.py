import pygame
import logging

from src.state import State
from src.screens.worldmap.resources import *
from src.worldmap.mappath import MapPath
from src.worldmap.landing import Landing
from src.worldmap.leveltile import LevelTile
from src.animatedsprite import AnimatedSprite
from src.worldmap.player import Player

class LoadMap(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.scene_name = args[0]
        self.player_start_position = args[1]

    def on_state_enter(self, world_map):
        # world_map.pause()
        self.game = world_map.game
        world_map.tile_layer_1 = {}
        world_map.tile_layer_2 = {}
        world_map.level_tiles = []
        world_map.map_path = []
        world_map.player = None
        world_map.overlay_layer_1 = {}
        world_map.scene_x = 0
        world_map.scene_y = 0
        world_map.scene_width = 0
        world_map.scene_height = 0

        for level in self.game.get_levels_from_world():
            if level["identifier"] == self.scene_name:
                '''this is where all of the code goes that you want to run when the world map scene loads. 
                this is where the loading starts '''
                world_map.scene_name = level["identifier"]
                world_map.scene_x = level["worldX"]
                world_map.scene_y = level["worldY"]
                world_map.scene_width = level["pxWid"]
                world_map.scene_height = level["pxHei"]
                level_layers = level["layerInstances"]

                for layer in level_layers:
                    if layer["__identifier"] == GROUND_1_LAYER_NAME:
                        world_map.tile_layer_1["tileset"] = layer["__tilesetRelPath"]
                        world_map.tile_layer_1["grid_size"] = layer["__gridSize"]
                        world_map.tile_layer_1["tiles"] = layer["gridTiles"]
                        world_map.load_tileset(f"{BASE_PATH}{world_map.tile_layer_1['tileset']}")
                    if layer["__identifier"] == GROUND_2_LAYER_NAME:
                        world_map.tile_layer_2["tileset"] = layer["__tilesetRelPath"]
                        world_map.tile_layer_2["grid_size"] = layer["__gridSize"]
                        world_map.tile_layer_2["tiles"] = layer["gridTiles"]
                        world_map.load_tileset(f"{BASE_PATH}{world_map.tile_layer_2['tileset']}")

                    if layer["__identifier"] == ENTITIES_LAYER_NAME:
                        entity_instances = layer["entityInstances"]
                        for entity in entity_instances:
                            if entity["__identifier"] == "world_map_object":
                                entity_properties = entity["fieldInstances"]
                                for property in entity_properties:
                                    if property["__value"] == "path":
                                        try:
                                            image = pygame.image.load(self.game.load_resource(MAP_PATH_IMAGE))
                                        except:
                                            logging.debug(f"could not load map path image!!!")
                                            image = pygame.surface.Surface([entity["width"], entity["height"]])
                                        new_map_path = MapPath(entity["__worldX"], entity["__worldY"],entity["width"], entity["height"], image)
                                        world_map.map_path.append(new_map_path)
                                    if property["__value"] == "landing":
                                        try:
                                            image = pygame.image.load(self.game.load_resource(MAP_LANDING_IMAGE))
                                        except:
                                            logging.debug(f"could not load map path image!!!")
                                            image = pygame.surface.Surface([entity["width"], entity["height"]])
                                        new_map_landing = Landing(entity["__worldX"], entity["__worldY"],entity["width"], entity["height"], image)
                                        world_map.landings.append(new_map_landing)
                                    if property["__value"] == "level_tile":
                                        level_name = None
                                        leads_to_scene = None
                                        for property in entity_properties:
                                            if property["__identifier"] == "level_name":
                                                level_name = property["__value"]
                                            if property["__identifier"] == "leads_to_scene":
                                                leads_to_scene = property["__value"]
                                        try:
                                            spritesheet = LEVEL_TILE_SPRITESHEET
                                        except:
                                            logging.debug(f"could not load map path image!!!")
                                            # spritesheet = pygame.surface.Surface([entity["width"], entity["height"]])
                                        
                                        animation = LEVEL_TILE_ANIMATION

                                        new_level_tile = LevelTile(self.game, level_name, entity["__worldX"], entity["__worldY"], entity["width"],spritesheet, animation, world_map.camera.surface, world_map.camera, leads_to_scene)
                                        # entity["__worldX"], entity["__worldY"],entity["width"], entity["height"], image
                                        world_map.level_tiles.append(new_level_tile)

                    if layer["__identifier"] == OVERLAY_1_LAYER_NAME:
                        world_map.overlay_layer_1["tileset"] = layer["__tilesetRelPath"]
                        world_map.overlay_layer_1["grid_size"] = layer["__gridSize"]
                        world_map.overlay_layer_1["tiles"] = layer["gridTiles"]
                        world_map.load_tileset(f"{BASE_PATH}{world_map.overlay_layer_1['tileset']}")
                break
        
        world_map.animated_tileset = AnimatedSprite(world_map.game, world_map.tilesets[f"{BASE_PATH}{world_map.tile_layer_1['tileset']}"])
        world_map.animated_tileset.load_spritesheet(MAP_ANIMATED_TILESET)
        world_map.animated_tileset.load_sprite_data(MAP_ANIMATION)
        world_map.animated_tileset.set_animation("idle")
        world_map.animated_tileset.play()

        # print(world_map.animated_tileset.spritesheet, world_map.animated_tileset.animations)
        
        world_map.player = Player(self.game, world_map, self.player_start_position[0], self.player_start_position[1],world_map.tile_size, world_map.tile_size, PLAYER_SPRITESHEET, PLAYER_ANIMATION,world_map.camera.surface,world_map.camera)
        
        world_map.camera.set_bounds(world_map.scene_x, world_map.scene_x + world_map.scene_width, world_map.scene_y, world_map.scene_y + world_map.scene_height)
        # world_map.camera.set_position(467,300)
        world_map.camera.center(self.player_start_position[0], self.player_start_position[1])
        world_map.fade_in()
    
    def draw(self, world_map):
        world_map.game.get_screen().fill("#000000")