import logging
import pygame

from res.settings import *
from res.framework.state import State
from res.framework.camera import Camera
from res.framework.worldmap.mappath import MapPath
from res.framework.worldmap.landing import Landing
from res.framework.worldmap.leveltile import LevelTile

WORLD_MAP_MUSIC = f"{MUSIC_PATH}/world_map.mp3"
BACKGROUND_IMAGE = f"{GRAPHICS_PATH}/backgrounds/world_map_background.png"
MAP_BOX = f"{GRAPHICS_PATH}/backgrounds/world_map_box.png"
MAP_POSITION = 91, 66

MAP_PATH_IMAGE = f"{GRAPHICS_PATH}/world_map/map_path.png"
MAP_LANDING_IMAGE = f"{GRAPHICS_PATH}/world_map/landing.png"

LEVEL_TILE_SPRITESHEET = f"{GRAPHICS_PATH}/world_map/level_tile.png"
LEVEL_TILE_ANIMATION = f"{ANIMATIONS_PATH}/level_tile.json"


class WorldMap(State):
    def on_state_enter(self, game):

        self.game = game

        self.camera = Camera(0, 0, WORLD_MAP_WIDTH, WORLD_MAP_HEIGHT)
        
        self.background_image = pygame.image.load(game.load_resource(BACKGROUND_IMAGE)).convert_alpha()
        self.background_image.set_alpha(160)
        self.map_box = pygame.image.load(game.load_resource(MAP_BOX)).convert_alpha()

        self.tilesets = {}

        self.tile_layer_1 = {}
        self.tile_layer_2 = {}
        self.level_tiles = []
        self.map_path = []
        self.landings = []
        self.player = None
        self.overlay_layer_1 = {}

        self.scene_x = 0
        self.scene_y = 0
        self.scene_width = 0
        self.scene_height = 0

        self.scene_name = None

        game.play_music(game.load_resource(WORLD_MAP_MUSIC))

        current_level = self.game.get_save_data('current_level')
        scene_name = None
        player_start_position = None

        if current_level == None:
            scene_name = WORLD_MAP_DEFAULT_SCENE
            for level in self.game.get_levels_from_world():
                if scene_name == level["identifier"]:
                    level_layers = level["layerInstances"]

                    for layer in level_layers:
                        if layer["__identifier"] == ENTITIES_LAYER_NAME:
                            entity_instances = layer["entityInstances"]
                            for entity in entity_instances:
                                if entity["__identifier"] == "world_map_object":
                                    entity_properties = entity["fieldInstances"]
                                    for property in entity_properties:
                                        if property["__value"] == "default_start":
                                            x = entity["__worldX"]
                                            y = entity["__worldY"]
                                            player_start_position = [x,y]

        else:
            for level in self.game.get_levels_from_world():
                level_name = level["identifier"]
                
                level_layers = level["layerInstances"]

                for layer in level_layers:
                    if layer["__identifier"] == ENTITIES_LAYER_NAME:
                        entity_instances = layer["entityInstances"]
                        for entity in entity_instances:
                            if entity["__identifier"] == "world_map_object":
                                entity_properties = entity["fieldInstances"]
                                for property in entity_properties:
                                    if property["__identifier"] == "level_name":
                                        if property["__value"] == current_level:
                                            scene_name = level_name
                                            x = entity["__worldX"]
                                            y = entity["__worldY"]
                                            player_start_position = [x,y]

        self.state = State(world_map_states)

        self.state.set_state(self, "load_map", scene_name, player_start_position)

        # self.state.start(self, "fade_in")
    
    def process_events(self, game):
        if game.game_should_quit():
            game.quit_game()
        self.state.process_events(self)

    def update(self, game):
        if self.level_tiles:
            for level_tile in self.level_tiles:
                level_tile.update()

        self.state.update(self)
    
    def draw(self, game):
        game.get_screen().fill("#000000")
        game.get_screen().blit(self.background_image, (0,0))
        game.get_screen().blit(self.map_box, (0,0))

        if self.tile_layer_1:
            tileset_path = game.load_resource(f"{BASE_PATH}{self.tile_layer_1['tileset']}")

            if tileset_path in self.tilesets:
                tileset_image = self.tilesets[tileset_path]
                for tile in self.tile_layer_1["tiles"]:
                    dest = tile["px"]
                    source = tile["src"]
                    grid_size = self.tile_layer_1["grid_size"]
                    camera_pos = self.camera.get_position()
                    dest[0] -= camera_pos[0]
                    dest[1] -= camera_pos[1]
                    self.camera.surface.blit(tileset_image,dest,[source[0], source[1], grid_size, grid_size])
            
        if self.tile_layer_2:
            tileset_path = game.load_resource(f"{BASE_PATH}{self.tile_layer_2['tileset']}")

            if tileset_path in self.tilesets:
                tileset_image = self.tilesets[tileset_path]
                for tile in self.tile_layer_2["tiles"]:
                    dest = tile["px"]
                    source = tile["src"]
                    grid_size = self.tile_layer_2["grid_size"]
                    camera_pos = self.camera.get_position()
                    dest[0] -= camera_pos[0]
                    dest[1] -= camera_pos[1]
                    self.camera.surface.blit(tileset_image,dest,[source[0], source[1], grid_size, grid_size])
        
        if self.map_path:
            for map_path in self.map_path:
                dest = [map_path.x, map_path.y]
                camera_pos = self.camera.get_position()
                dest[0] -= camera_pos[0]
                dest[1] -= camera_pos[1]
                self.camera.surface.blit(map_path.image, dest)

        if self.landings:
            for landing in self.landings:
                dest = [landing.x, landing.y]
                camera_pos = self.camera.get_position()
                dest[0] -= camera_pos[0]
                dest[1] -= camera_pos[1]
                self.camera.surface.blit(landing.image, dest)
        
        if self.level_tiles:
            for level_tile in self.level_tiles:
                level_tile.draw()
        
        if self.overlay_layer_1:
            tileset_path = game.load_resource(f"{BASE_PATH}{self.overlay_layer_1['tileset']}")

            if tileset_path in self.tilesets:  
                tileset_image = self.tilesets[tileset_path]
                for tile in self.overlay_layer_1["tiles"]:
                    dest = tile["px"]
                    source = tile["src"]
                    grid_size = self.overlay_layer_1["grid_size"]
                    camera_pos = self.camera.get_position()
                    dest[0] -= camera_pos[0]
                    dest[1] -= camera_pos[1]
                    self.camera.surface.blit(tileset_image,dest,[source[0], source[1], grid_size, grid_size])

        self.game.get_screen().blit(self.camera.surface, MAP_POSITION)
        
        self.state.draw(self)

        # print(self.game.get_fps())
    
    def load_tileset(self, image_path):
        if image_path not in self.tilesets:
            if os.path.exists(image_path):
                new_tileset_surface = pygame.image.load(image_path).convert_alpha()
                self.tilesets[image_path] = new_tileset_surface
            else:
                logging.debug(f"could not load tileset! image path {image_path} does not exist!")
        else:
            if os.path.exists(image_path):
                new_tileset_surface = pygame.image.load(image_path).convert_alpha()
                self.tilesets[image_path] = new_tileset_surface
            else:
                logging.debug(f"could not load tileset! image path {image_path} does not exist!")
    
    def fade_in(self):
        self.state.start(self, "fade_in")


class LoadMap(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.scene_name = args[0]
        self.player_start_position = args[1]

    def on_state_enter(self, world_map):
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
                        world_map.load_tileset(self.game.load_resource(f"{BASE_PATH}{world_map.tile_layer_1['tileset']}"))
                    if layer["__identifier"] == GROUND_2_LAYER_NAME:
                        world_map.tile_layer_2["tileset"] = layer["__tilesetRelPath"]
                        world_map.tile_layer_2["grid_size"] = layer["__gridSize"]
                        world_map.tile_layer_2["tiles"] = layer["gridTiles"]
                        world_map.load_tileset(self.game.load_resource(f"{BASE_PATH}{world_map.tile_layer_2['tileset']}"))

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
                                        world_map.map_path.append(new_map_landing)
                                    if property["__value"] == "level_tile":
                                        level_name = None
                                        for property in entity_properties:
                                            if property["__identifier"] == "level_name":
                                                level_name = property["__value"]
                                        try:
                                            spritesheet = self.game.load_resource(LEVEL_TILE_SPRITESHEET)
                                        except:
                                            logging.debug(f"could not load map path image!!!")
                                            # spritesheet = pygame.surface.Surface([entity["width"], entity["height"]])
                                        
                                        animation = self.game.load_resource(LEVEL_TILE_ANIMATION)

                                        new_level_tile = LevelTile(self.game, level_name, entity["__worldX"], entity["__worldY"], entity["width"],spritesheet, animation, world_map.camera.surface, world_map.camera)
                                        # entity["__worldX"], entity["__worldY"],entity["width"], entity["height"], image
                                        world_map.level_tiles.append(new_level_tile)

                    if layer["__identifier"] == OVERLAY_1_LAYER_NAME:
                        world_map.overlay_layer_1["tileset"] = layer["__tilesetRelPath"]
                        world_map.overlay_layer_1["grid_size"] = layer["__gridSize"]
                        world_map.overlay_layer_1["tiles"] = layer["gridTiles"]
                        world_map.load_tileset(self.game.load_resource(f"{BASE_PATH}{world_map.overlay_layer_1['tileset']}"))
                break
        
        world_map.camera.set_bounds(world_map.scene_x, world_map.scene_x + world_map.scene_width, world_map.scene_y, world_map.scene_y + world_map.scene_height)
        # world_map.camera.set_position(467,300)
        world_map.camera.center(self.player_start_position[0], self.player_start_position[1])
        world_map.fade_in()
    
    def draw(self, world_map):
        world_map.game.get_screen().fill("#000000")
        

class FadeIn(State):
    def on_state_enter(self, world_map):
        self.min_fade = 0
        self.max_fade = 255
        self.fade = self.min_fade
        self.fade_step = 5
    
    def draw(self, world_map):
        if self.fade < self.max_fade:
            world_map.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
            self.fade += self.fade_step
        else:
            
            piss = 0



world_map_states = {
            "fade_in" : FadeIn,
            "load_map" : LoadMap
}