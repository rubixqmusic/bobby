import logging
import pygame

from res.settings import *
from res.framework.state import State
from res.framework.camera import Camera

WORLD_MAP_MUSIC = f"{MUSIC_PATH}/world_map.mp3"
BACKGROUND_IMAGE = f"{GRAPHICS_PATH}/backgrounds/world_map_background.png"
MAP_BOX = f"{GRAPHICS_PATH}/backgrounds/world_map_box.png"


class WorldMap(State):
    def on_state_enter(self, game):

        self.game = game

        self.camera = Camera(0, 0, WORLD_MAP_WIDTH, WORLD_MAP_HEIGHT)
        
        self.background_image = pygame.image.load(game.load_resource(BACKGROUND_IMAGE)).convert_alpha()
        self.background_image.set_alpha(160)
        self.map_box = pygame.image.load(game.load_resource(MAP_BOX)).convert_alpha()

        self.tilesets = {}

        self.tile_layer_1 = None
        self.tile_layer_2 = None
        self.level_tiles = []
        self.map_path = []
        self.player = None
        self.overlay_layer_1 = None

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


        print(current_level, scene_name, player_start_position)

        self.state = State(world_map_states)

        # self.state.set_state(self, "load_map", scene_name, player_start_position)

        self.state.start(self, "fade_in")
    
    def process_events(self, game):
        if game.game_should_quit():
            game.quit_game()
        self.state.process_events(self)

    def update(self, game):
        self.state.update(self)
    
    def draw(self, game):
        game.get_screen().fill("#000000")
        game.get_screen().blit(self.background_image, (0,0))
        game.get_screen().blit(self.map_box, (0,0))
        self.state.draw(self)


class LoadMap(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.scene_name = args[0]
        self.player_start_position = args[1]

    def on_state_enter(self, world_map):
        self.game = world_map.game

        for level in self.game.get_levels_from_world():
            if level["identifier"] == self.scene_name:
                level_layers = level["layerInstances"]



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