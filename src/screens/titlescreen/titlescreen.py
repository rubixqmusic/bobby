import logging
import pygame
import math
import json

from settings import *
from src.screens.titlescreen.resources import *
from src.screens.titlescreen.screenstates import title_screen_states
from src.state import State
from src.components.animatedsprite import AnimatedSprite


class TitleScreen(State):
    def on_state_enter(self, game):

        game.set_current_save_file("")

        
        
        self.sine_degrees = 0
        self.grow_factor = 0
        self.game = game

        # self.background_scroll_step = 0

        # self.background_image = pygame.image.load(self.game.load_resource(background_image_path)).convert_alpha()
        # self.background_image.set_alpha(BACKGROUND_ALPHA)
        # self.background_image_wrap = pygame.image.load(self.game.load_resource(background_image_path)).convert_alpha()
        # self.background_image_wrap.set_alpha(BACKGROUND_ALPHA)

        # self.trees_image = pygame.image.load(self.game.load_resource(trees_image_path)).convert_alpha()
        # self.trees_image_wrap = pygame.image.load(self.game.load_resource(trees_image_path)).convert_alpha()

        self.menu_selection_font = pygame.font.Font(game.load_resource(menu_selection_font_path),menu_selection_text_size)
        self.licensed_by_kablio_font = pygame.font.Font(game.load_resource(menu_selection_font_path), licensed_by_kablio_text_size)

        # self.background_image_position = [0,0]
        # self.background_image_wrap_position = [self.background_image_position[0] + self.background_image.get_width(), self.background_image_position[1]]
        
        # self.trees_image_position = [0,0]
        # self.trees_image_wrap_position = [self.trees_image_position[0] + self.trees_image.get_width(), self.trees_image_position[1]]

        self.title_text_image = pygame.image.load(self.game.load_resource(title_screen_text_path)).convert_alpha()
        self.licensed_by_kablio_text_surface = self.licensed_by_kablio_font.render(licensed_by_kablio_text,True,main_text_color)

        scene_name = game.resource_config["TITLE_SCREEN_SCENE"]

        self.overlay_transition = AnimatedSprite()
        self.overlay_transition.set_draw_target(self.game.get_screen())
        self.overlay_transition.load_animation(self.game.load_resource(OVERLAY_TRANSITION_ANIMATION))
        self.overlay_transition.load_spritesheet(self.game.load_resource(OVERLAY_TRANSITION_SPRITESHEET))
        self.overlay_transition.set_animation(MONEY_IN_ANIMATION)

        
        self.animated_background = None
        self.background_1 = None
        self.background_2 = None
        self.background_3 = None
        self.ground = None
        self.dim_color = pygame.surface.Surface(SCREEN_SIZE)
        self.dim_color.set_alpha(100)

        scene_data = self.load_scene_data(scene_name)

        game.play_music(title_screen_music_path)
        
        self.state = State(title_screen_states)

        self.money_in()
        # self.state.start(self, "money_in")

    def process_events(self, game):
        self.state.process_events(self)

    def update(self, game):
        delta = game.get_delta_time()
        self.grow_factor = int(math.sin(self.sine_degrees) * max_text_grow)
        self.sine_degrees += text_grow_step_size%max_text_grow

        # self.background_scroll_step += 1
        # self.background_scroll_step = self.background_scroll_step%BACKGROUND_SCROLL_SPEED

        # if self.background_scroll_step == 0:
        #     self.background_image_position[0] -= 1

        # if self.background_image_position[0] + self.background_image.get_width() < 0:
        #     self.background_image_position[0] += self.background_image.get_width()
        # self.background_image_wrap_position[0] = self.background_image_position[0] + self.background_image.get_width()

        # self.trees_image_position[0] -= scroll_speed
        # if self.trees_image_position[0] + self.trees_image.get_width() < 0:
        #     self.trees_image_position[0] += self.trees_image.get_width()

        # self.trees_image_wrap_position[0] = self.trees_image_position[0] + self.trees_image.get_width()

        self.animated_background.update(delta)

        for bg in [self.background_1, self.background_2, self.background_3]:
            if bg:
                bg["position"][0] -= (SCROLL_SPEED * bg["parallax_x"]) * delta
                if bg["position"][0] + bg["image"].get_width() < 0:
                    bg["position"][0] += bg["image"].get_width()
        
        if self.ground:
            self.ground["position"][0] -= int((SCROLL_SPEED * 0.17) * delta)
            if self.ground["position"][0] + self.ground["image"].get_width() < 0:
                self.ground["position"][0] += self.ground["image"].get_width()


        self.state.update(self)

    def draw(self, game):
        text_rect = self.licensed_by_kablio_text_surface.get_rect(center=(SCREEN_WIDTH/2, licensed_by_kablio_text_y_position))
        game.get_screen().fill("#000000")

        self.animated_background.draw()
        for bg in [self.background_1, self.background_2, self.background_3]:
            game.get_screen().blit(bg["image"], bg["position"])
            game.get_screen().blit(bg["image"], [bg["position"][0] + bg["image"].get_width(), bg["position"][1]])

        game.get_screen().blit(self.ground["image"], self.ground["position"])
        game.get_screen().blit(self.ground["image"], [self.ground["position"][0] + self.ground["image"].get_width(), self.ground["position"][1]])
        game.get_screen().blit(self.dim_color, (0,0))
        # print(self.ground["image"])
        # print(self.ground["position"])
        # game.get_screen().blit(self.background_image, self.background_image_position)
        # game.get_screen().blit(self.background_image_wrap, self.background_image_wrap_position)
        # game.get_screen().blit(self.trees_image, self.trees_image_position)
        # game.get_screen().blit(self.trees_image_wrap, self.trees_image_wrap_position)

        game.get_screen().blit(self.title_text_image, (0,0))
        game.get_screen().blit(self.licensed_by_kablio_text_surface, text_rect)

        self.state.draw(self)


    def go_to_file_select_screen(self):
        self.state.set_state(self, "go_to_file_select_screen")

    def start_game_or_quit(self):
        self.state.set_state(self, "start_game_or_quit")

    def go_to_settings_screen(self):
        self.state.set_state(self, "go_to_settings_screen")

    def fade_out_and_quit(self):
        self.state.set_state(self, "fade_out_and_quit")
    
    def money_in(self):
        self.state.set_state(self, "money_in")

    
    def load_scene_data(self, scene_name):
        for scene in self.game.get_levels_from_world():

            '''here is where the level loading begins'''

            if scene["identifier"] == scene_name:
                for scene_property in scene["fieldInstances"]:
                    if scene_property["__identifier"] == "music":
                        music_path = f"{MUSIC_PATH}/{scene_property['__value']}{MUSIC_FILE_EXTENSION}"
                        if self.game.resource_exists(music_path):
                            self.game.play_music(music_path)
                    if scene_property["__identifier"] == "animated_background":
                        if scene_property["__value"]:
                            background_data = json.loads(scene_property["__value"])

                            if "image" in background_data and "animation" in background_data:

                                bg_image_path = f"{GRAPHICS_PATH}/animated_backgrounds/{background_data['image']}{BACKGROUND_IMAGE_FILE_EXTENSION}"
                                bg_animation_data = f"{ANIMATIONS_PATH}/{background_data['animation']}.json"
                                
                                
                                if self.game.resource_exists(bg_image_path) and self.game.resource_exists(bg_animation_data):
                                    self.animated_background = AnimatedSprite()
                                    self.animated_background.set_draw_target(self.game.get_screen())
                                    self.animated_background.load_spritesheet(self.game.load_resource(bg_image_path))
                                    self.animated_background.load_animation(self.game.load_resource(bg_animation_data))
                                    self.animated_background.set_animation("idle")
                                    self.animated_background.set_position(0,0)
                                    self.animated_background.play()
                    
                    if scene_property["__identifier"] == "background_1":
                        if scene_property["__value"]:
                            background_data = json.loads(scene_property["__value"])
                            if "image" in background_data:
                                bg_image_path = f"{GRAPHICS_PATH}/scene_backgrounds/{background_data['image']}{BACKGROUND_IMAGE_FILE_EXTENSION}"
                                
                                if self.game.resource_exists(bg_image_path):
                                    self.background_1 = {}
                                    self.background_1["position"] = [0,0]
                                    self.background_1["parallax_x"] = 0.0
                                    self.background_1["parallax_y"] = 0.0
                                    self.background_1["image"] = pygame.image.load(self.game.load_resource(bg_image_path))
                            
                    if scene_property["__identifier"] == "background_2":
                        if scene_property["__value"]:
                            background_data = json.loads(scene_property["__value"])
                            if "image" in background_data:
                                bg_image_path = f"{GRAPHICS_PATH}/scene_backgrounds/{background_data['image']}{BACKGROUND_IMAGE_FILE_EXTENSION}"
                                
                                if self.game.resource_exists(bg_image_path):
                                    self.background_2 = {}
                                    self.background_2["position"] = [0,0]
                                    self.background_2["parallax_x"] = 0.05
                                    self.background_2["parallax_y"] = 0.0
                                    self.background_2["image"] = pygame.image.load(self.game.load_resource(bg_image_path))

                    if scene_property["__identifier"] == "background_3":
                        if scene_property["__value"]:
                            background_data = json.loads(scene_property["__value"])
                            if "image" in background_data:
                                bg_image_path = f"{GRAPHICS_PATH}/scene_backgrounds/{background_data['image']}{BACKGROUND_IMAGE_FILE_EXTENSION}"
                                
                                if self.game.resource_exists(bg_image_path):
                                    self.background_3 = {}
                                    self.background_3["position"] = [0,0]
                                    self.background_3["parallax_x"] = 0.1
                                    self.background_3["parallax_y"] = 0.0
                                    self.background_3["image"] = pygame.image.load(self.game.load_resource(bg_image_path))
                
                ground_layer_width = scene["pxWid"]
                ground_layer_height = scene["pxHei"]
                self.ground = {}
                self.ground["image"] = pygame.surface.Surface((ground_layer_width, ground_layer_height))
                if self.ground["image"]:
                    self.ground["image"].set_colorkey((0,0,0))
                self.ground["position"] = [0,-SCREEN_HEIGHT]

                for layer in scene["layerInstances"]:

                    if layer["__identifier"] == GROUND_2_LAYER_NAME:
                        tileset = f"{BASE_PATH}{layer['__tilesetRelPath']}"    
                        ground_tileset = pygame.image.load(self.game.load_resource(tileset))
                        tiles = layer["gridTiles"]
                        tile_size = layer["__gridSize"]

                        for tile in tiles:
                            dest_rect = pygame.rect.Rect(tile["px"][0], tile["px"][1], tile_size, tile_size)
                            source_rect = pygame.rect.Rect(tile["src"][0], tile["src"][1], tile_size, tile_size)
                            # pygame.draw.rect(self.ground["image"], (255,0,0), dest_rect, 3)
                            self.ground["image"].blit(ground_tileset, dest_rect, source_rect)

                        for layer in scene["layerInstances"]:
# 
                            if layer["__identifier"] == MAIN_GROUND_LAYER_NAME:
                                tileset = f"{BASE_PATH}{layer['__tilesetRelPath']}"    
                                ground_tileset = pygame.image.load(self.game.load_resource(tileset))
                                if ground_tileset:
                                    ground_tileset.convert_alpha()
                                tiles = layer["autoLayerTiles"]
                                tile_size = layer["__gridSize"]
                                for tile in tiles:
                                    source_rect = pygame.rect.Rect(tile["src"][0], tile["src"][1], tile_size, tile_size)
                                    self.ground["image"].blit(ground_tileset, [tile["px"][0], tile["px"][1]], source_rect)


