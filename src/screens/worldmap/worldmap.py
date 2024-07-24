import logging
import pygame
import math

from settings import *
from src.state import State
from src.camera import Camera
from src.screens.worldmap.resources import *
from src.screens.worldmap.screenstates import world_map_states


class WorldMap(State):
    def on_state_enter(self, game):
        
        self.game = game
        self.paused = False

        self.sine_degrees = 0
        self.grow_factor = 0

        self.animated_tileset = None

        self.camera = Camera(0, 0, WORLD_MAP_WIDTH, WORLD_MAP_HEIGHT)
        
        self.background_image = pygame.image.load(game.load_resource(BACKGROUND_IMAGE)).convert_alpha()
        self.background_image.set_alpha(200)
        self.map_box = pygame.image.load(game.load_resource(MAP_BOX)).convert_alpha()

        self.tilesets = {}
        self.tile_size = 16

        self.font_size = 12
        self.font_color = GOLD_COLOR
        self.font = pygame.font.Font(game.load_resource(MAP_FONT), self.font_size)

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
        self.level_name = None
        self.level_name_surface = None
        self.percent_to_plan_surface = None

        game.play_music(WORLD_MAP_MUSIC)

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

        self.load_map(scene_name, player_start_position)
    
    def process_events(self, game):
        if game.game_should_quit():
            game.quit_game()
        self.state.process_events(self)

    def update(self, game):

        self.grow_factor = int(math.sin(self.sine_degrees) * MAX_TEXT_GROW)
        self.sine_degrees += TEXT_GROW_STEP_SIZE%MAX_TEXT_GROW

    
        if not self.paused:
            if self.animated_tileset:
                self.animated_tileset.update()

            if self.level_tiles:
                for level_tile in self.level_tiles:
                    level_tile.update()
            
            if self.player:
                self.player.update()

        self.state.update(self)
    
    def draw(self, game):

        if self.animated_tileset:
            self.animated_tileset.draw()

        game.get_screen().fill("#000000")
        game.get_screen().blit(self.background_image, (0,0))
        game.get_screen().blit(self.map_box, (0,0))
        self.camera.surface.fill("#000000")


        # future you: to solve the animated tile problem, just set an animated sprites draw target to the tileset's image
        # in the 'tilesets' dictionary. then call update, and draw, and then blit from the tileset image

        if self.tile_layer_1:
            
            tileset_path = f"{BASE_PATH}{self.tile_layer_1['tileset']}"

            if tileset_path in self.tilesets:
                tileset_image = self.tilesets[tileset_path]
                for tile in self.tile_layer_1["tiles"]:
                    dest = tile["px"]
                    source = tile["src"]
                    grid_size = self.tile_layer_1["grid_size"]
                    camera_pos = self.camera.get_position()
                    draw_x = dest[0] - camera_pos[0]
                    draw_y = dest[1] - camera_pos[1]
                    self.camera.surface.blit(tileset_image,[draw_x,draw_y],[source[0], source[1], grid_size, grid_size])

    
            
        if self.tile_layer_2:
            tileset_path = f"{BASE_PATH}{self.tile_layer_2['tileset']}"

            if tileset_path in self.tilesets:
                tileset_image = self.tilesets[tileset_path]
                for tile in self.tile_layer_2["tiles"]:
                    dest = tile["px"]
                    source = tile["src"]
                    grid_size = self.tile_layer_2["grid_size"]
                    camera_pos = self.camera.get_position()
                    draw_x = dest[0] - camera_pos[0]
                    draw_y = dest[1] - camera_pos[1]
                    self.camera.surface.blit(tileset_image,[draw_x,draw_y],[source[0], source[1], grid_size, grid_size])
        
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
        
        if self.player:
            self.player.draw()
        
        if self.overlay_layer_1:
            tileset_path = f"{BASE_PATH}{self.overlay_layer_1['tileset']}"

            if tileset_path in self.tilesets:  
                tileset_image = self.tilesets[tileset_path]
                for tile in self.overlay_layer_1["tiles"]:
                    dest = tile["px"]
                    source = tile["src"]
                    grid_size = self.overlay_layer_1["grid_size"]
                    camera_pos = self.camera.get_position()
                    draw_x = dest[0] - camera_pos[0]
                    draw_y = dest[1] - camera_pos[1]
                    self.camera.surface.blit(tileset_image,[draw_x,draw_y],[source[0], source[1], grid_size, grid_size])

        self.game.get_screen().blit(self.camera.surface, MAP_POSITION)

        if self.level_name_surface:
            level_name_rect = self.level_name_surface.get_rect(center=LEVEL_NAME_CENTER)
            self.game.get_screen().blit(self.level_name_surface, level_name_rect)
        if self.percent_to_plan_surface:
            percent_rect = self.percent_to_plan_surface.get_rect(center=PERCENT_TO_PLAN_CENTER)
            self.game.get_screen().blit(self.percent_to_plan_surface, percent_rect)
        
        self.state.draw(self)


    def load_tileset(self, image_path):
        if image_path not in self.tilesets:
            if self.game.resource_exists(image_path):
                new_tileset_surface = pygame.image.load(self.game.load_resource(image_path)).convert_alpha()
                self.tilesets[image_path] = new_tileset_surface
            else:
                logging.debug(f"could not load tileset! image path {image_path} does not exist!")
        else:
            if self.game.resource_exists(image_path):
                new_tileset_surface = pygame.image.load(self.game.load_resource(image_path)).convert_alpha()
                self.tilesets[image_path] = new_tileset_surface
            else:
                logging.debug(f"could not load tileset! image path {image_path} does not exist!")
    

    def set_current_level(self, level_name):
        if level_name == None:
            return
        if level_name == "landing":
            self.level_name = "landing"
            self.level_name_surface = None
            self.percent_to_plan_surface = None
            return
        level_data = self.game.get_level_data(level_name)
        if level_data:
            self.level_name = level_name
            self.level_name_surface = self.font.render(f"{level_data['display_name']}",True,self.font_color)
            self.percent_to_plan_surface = self.font.render(f"{level_data['percent_to_plan']}/100 %",True,self.font_color)

    def pause(self):
        self.paused = True
    
    def unpause(self):
        self.paused = False

    def load_map(self, scene_name, player_start_position):
        self.pause() 
        self.state.set_state(self, "load_map", scene_name, player_start_position)   
    
    def fade_in(self):
        self.pause()
        self.state.set_state(self, "fade_in")

    def map_active(self):
        self.unpause()
        self.state.set_state(self, "map_active")
    
    def start_level(self):
        self.game.play_sound(LEVEL_START_SOUND)
        self.game.stop_music()
        self.game.set_save_data("current_level", self.level_name)
        self.state.set_state(self, "start_level")

    def quit_menu(self):
        self.pause()
        self.state.set_state(self, "quit_menu")
    
    def quit_to_main_menu(self):
        self.game.save_game()
        self.state.set_state(self, "quit_to_main_menu")

    def load_scene(self):
        for level in self.level_tiles:
            if level.level_name == self.level_name:
                if level.leads_to_scene == None:
                    return
                else:
                    leads_to_scene_data = level.leads_to_scene
                    scene_and_starting_position = self.game.get_scene_and_starting_position_from_iid(leads_to_scene_data["levelIid"], leads_to_scene_data["entityIid"])
                    if scene_and_starting_position == None:
                        return
                    else:
                        self.game.load_level(scene_and_starting_position[0], scene_and_starting_position[1], DEFAULT_TRANSITION)

        


