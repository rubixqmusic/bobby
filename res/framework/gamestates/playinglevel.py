import logging
import pygame
import math

from res.settings import *
from res.framework.state import State
from res.framework.camera import Camera
from res.framework.animatedsprite import AnimatedSprite

TRANSITION_SPRITESHEET = f"{GRAPHICS_PATH}/screen_transitions/screen_transitions.png"
TRANSITION_ANIMATION = f"{ANIMATIONS_PATH}/screen_transitions.json"

DEFAULT_LEVEL_MUSIC = f"{MUSIC_PATH}/main_level.mp3"

LEVEL_MUSIC = {
                "default" : f"{MUSIC_PATH}/main_level.mp3"
               }

BACKGROUND_IMAGE_FILE_EXTENSION = f".png"

class PlayingLevel(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.level_name = args[0]

        self.player_start_position = args[1]
        self.transition_in = args[2]
        self.transition_out = None
        self.paused = False
        self.clear_scene()
    
    def clear_scene(self):
        self.width = None
        self.height = None
        self.tilesets = {}
        self.bg_color = f"#000000"
        self.bg_image = None
        self.bg_1 = None
        self.bg_2 = None
        self.bg_3 = None
        self.ground_1 = {}
        self.ground_2 = {}
        self.main_ground = {}
        self.objects = {}
        self.player = None
        self.overlay_1 = {}
        self.overlay_2 = {}
        self.fg_1 = {}
        self.fg_2 = {}

    def on_state_enter(self, game):
        self.game = game
        self.camera = Camera(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.transition_overlay = AnimatedSprite(self.game, self.game.get_screen())
        self.transition_overlay.load_spritesheet(TRANSITION_SPRITESHEET)
        self.transition_overlay.load_sprite_data(TRANSITION_ANIMATION)
        self.transition_overlay.set_animation("idle")

        self.state = State(level_states)

        # level_name = self.level_name
        self.load_scene(self.level_name, self.player_start_position, None, "money_in")

    def process_events(self, game):
        if game.game_should_quit():
            game.quit_game()
        # self.state.process_events(self)
    
    def update(self, game):
        if not self.paused:
            CAMSPD = 3
            if game.is_button_pressed(RIGHT_BUTTON):
                self.camera.move(CAMSPD,0)
            if game.is_button_pressed(LEFT_BUTTON):
                self.camera.move(-CAMSPD,0)
            if game.is_button_pressed(UP_BUTTON):
                self.camera.move(0,-CAMSPD)
            if game.is_button_pressed(DOWN_BUTTON):
                self.camera.move(0, CAMSPD)
            
            
            if self.bg_image:
                self.bg_image.update()

            self.state.update(self)

    def draw(self, game):
        game.get_screen().fill(self.bg_color)
        
        if self.bg_image:
            # self.camera.surface.blit(self.bg_image, [0,0])
            self.bg_image.draw()
        
        if self.bg_1:
            camera_pos = self.camera.get_position()
            parallax_x = int(camera_pos[0] * self.bg_1["parallax_x"])
            parallax_y = int(camera_pos[1] * self.bg_1["parallax_y"])

            draw_x = 0 - parallax_x
            draw_y = 0 - parallax_y

            if draw_x < camera_pos[0]:
                draw_x -= self.bg_1["image"].get_width()
            if draw_x > camera_pos[0] + self.bg_1["image"].get_width():
                draw_x += self.bg_1["image"].get_width()

            wrap_x = draw_x + self.bg_1["image"].get_width()  

            self.camera.surface.blit(self.bg_1["image"], [draw_x,draw_y])
            self.camera.surface.blit(self.bg_1["image"], [wrap_x,draw_y])
        
        if self.bg_2:

            camera_pos = self.camera.get_position()

            # print(camera_pos)

            parallax_x = int(camera_pos[0] * self.bg_2["parallax_x"])
            parallax_y = int(camera_pos[1] * self.bg_2["parallax_y"])

            draw_x = 0 - parallax_x
            # draw_y = 0 - parallax_y 
            draw_y = 0 - parallax_y#camera_pos[1]  

            wrap_x = draw_x + self.bg_2["image"].get_width()  

            # print(self.game.get_fps())

                      
            self.camera.surface.blit(self.bg_2["image"], [draw_x,draw_y])
            self.camera.surface.blit(self.bg_2["image"], [wrap_x ,draw_y])

        if self.bg_3:
            camera_pos = self.camera.get_position()

            # print(camera_pos)

            parallax_x = int(camera_pos[0] * self.bg_3["parallax_x"]) % self.bg_3["image"].get_width()  
            parallax_y = int(camera_pos[1] * self.bg_3["parallax_y"])

            draw_x = 1 - parallax_x
            # draw_y = 0 - parallax_y 
            draw_y = 0 - parallax_y#camera_pos[1]  

            wrap_x = draw_x + self.bg_3["image"].get_width()  

            # print(self.game.get_fps())

                      
            self.camera.surface.blit(self.bg_3["image"], [draw_x,draw_y])
            self.camera.surface.blit(self.bg_3["image"], [wrap_x ,draw_y])
        
        if self.ground_2:
            tileset_path = f"{BASE_PATH}{self.ground_2['tileset']}"

            if tileset_path in self.tilesets:
                tileset_image = self.tilesets[tileset_path]
                for tile in self.ground_2["tiles"]:
                    dest = tile["px"]
                    source = tile["src"]
                    grid_size = self.main_ground["grid_size"]
                    camera_pos = self.camera.get_position()
                    draw_x = dest[0] - camera_pos[0]
                    draw_y = dest[1] - camera_pos[1]
                    self.camera.surface.blit(tileset_image,[draw_x,draw_y],[source[0], source[1], grid_size, grid_size])

        if self.main_ground:
            tileset_path = f"{BASE_PATH}{self.main_ground['tileset']}"

            if tileset_path in self.tilesets:
                tileset_image = self.tilesets[tileset_path]
                for tile in self.main_ground["tiles"]:
                    dest = tile["px"]
                    source = tile["src"]
                    grid_size = self.main_ground["grid_size"]
                    camera_pos = self.camera.get_position()
                    draw_x = dest[0] - camera_pos[0]
                    draw_y = dest[1] - camera_pos[1]
                    self.camera.surface.blit(tileset_image,[draw_x,draw_y],[source[0], source[1], grid_size, grid_size])
        
        self.game.get_screen().blit(self.camera.surface, [0,0])

        self.state.draw(self)

    def pause(self):
        self.paused = True
    
    def unpause(self):
        self.paused = False

    def load_scene(self, level_name, player_start_position, transition_out=None, transition_in=None):
        self.level_name = level_name
        self.player_start_position = player_start_position
        self.transition_out = transition_out
        self.transition_in = transition_in

        if self.transition_out == None:
            self.state.set_state(self,"load_scene", level_name, self.player_start_position, self.transition_in)
    
    def money_in_transition(self):
        self.state.set_state(self, "money_in_transition")
    
    def start_scene(self):
        self.state.set_state(self, "level_active")


class LoadScene(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.level_name = args[0]
        self.player_start_position = args[1]
        self.transition_in = args[2]

    def on_state_enter(self, level: PlayingLevel): 
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
                
                print(level.tilesets)

                level.camera.set_bounds(0, level.width, 0, level.height)
                level.camera.center(self.player_start_position[0], self.player_start_position[1])



        if self.transition_in == "money_in":
            level.money_in_transition()


class MoneyInTransition(State):
    def on_state_enter(self, level: PlayingLevel):
        self.level = level
        level.transition_overlay.set_animation("money_in")
        level.transition_overlay.play()

        self.level.transition_overlay.animation_finished.attach(self, "animation_finished")

    
    def update(self, level: PlayingLevel):
        level.transition_overlay.update()
    
    def draw(self, level: PlayingLevel):
        level.transition_overlay.draw()
    
    def animation_finished(self, animation):
        self.start_scene()

    def start_scene(self):
        self.level.start_scene()
    
    def on_state_exit(self, level: PlayingLevel):
        level.transition_overlay.animation_finished.detach(self)

        


class LevelActive(State):
    def on_state_enter(self, level):
    
        print("LEVEL IS NOW ACTIVE")



level_states = {
                "load_scene" : LoadScene,
                "money_in_transition" : MoneyInTransition,
                "level_active" : LevelActive
                }
        