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
        self.bg_color = f"#000000"
        self.bg_image = None
        self.bg_1 = None
        self.bg_2 = None
        self.bg_3 = None
        self.ground_1 = None
        self.ground_2 = None
        self.main_ground = None
        self.objects = None
        self.player = None
        self.overlay_1 = None
        self.overlay_2 = None
        self.fg_1 = None
        self.fg_2 = None

    def on_state_enter(self, game):
        self.game = game
        self.camera = Camera(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.transition_overlay = AnimatedSprite(self.game, self.game.get_screen())
        self.transition_overlay.load_spritesheet(self.game.load_resource(TRANSITION_SPRITESHEET))
        self.transition_overlay.load_sprite_data(self.game.load_resource(TRANSITION_ANIMATION))
        self.transition_overlay.set_animation("idle")

        self.state = State(level_states)

        # level_name = self.level_name
        self.load_scene(self.level_name, self.player_start_position, None, "money_in")

    def process_events(self, game):
        if game.game_should_quit():
            game.quit_game()
        # self.state.process_events(self)
    
    def update(self, game):
        if game.is_button_pressed(RIGHT_BUTTON):
            self.camera.move(10,0)
        if game.is_button_pressed(LEFT_BUTTON):
            self.camera.move(-10,0)


        self.state.update(self)

    def draw(self, game):
        game.get_screen().fill(self.bg_color)
        
        if self.bg_image:
            game.get_screen().blit(self.bg_image, [0,0])
        
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

            game.get_screen().blit(self.bg_1["image"], [draw_x,draw_y])
            game.get_screen().blit(self.bg_1["image"], [wrap_x,draw_y])
        
        if self.bg_2:
            camera_pos = self.camera.get_position()
            parallax_x = int(camera_pos[0] * self.bg_2["parallax_x"])
            parallax_y = int(camera_pos[1] * self.bg_2["parallax_y"])
            print(f"parallax_x: {parallax_x}")

            draw_x = 0 - parallax_x
            draw_y = 0 - parallax_y

            wrap_x = draw_x + self.bg_2["image"].get_width()  

            print(f"draw x and wrap x: {draw_x, wrap_x}")
            print(f"camera pos: {self.camera.get_position()}")
                      
            game.get_screen().blit(self.bg_2["image"], [draw_x,draw_y])
            game.get_screen().blit(self.bg_2["image"], [wrap_x ,draw_y])

        if self.bg_3:
            game.get_screen().blit(self.bg_3["image"], [0,0])

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
                            level.game.play_music(level.game.load_resource(LEVEL_MUSIC[level_property["__value"]]))
                    if level_property["__identifier"] == "background":
                        if level_property["__value"]:
                            bg_image_path = level.game.load_resource(f"{GRAPHICS_PATH}/scene_backgrounds/bg_image/{level_property['__value']}{BACKGROUND_IMAGE_FILE_EXTENSION}")
                            
                            if os.path.exists(bg_image_path):
                                level.bg_image = pygame.image.load(bg_image_path)
                            
                            bg_image_path = level.game.load_resource(f"{GRAPHICS_PATH}/scene_backgrounds/bg_1/{level_property['__value']}{BACKGROUND_IMAGE_FILE_EXTENSION}")
                            
                            if os.path.exists(bg_image_path):
                                level.bg_1 = {}
                                level.bg_1["parallax_x"] = 0.05
                                level.bg_1["parallax_y"] = 0.1
                                level.bg_1["image"] = pygame.image.load(bg_image_path)
                            
                            bg_image_path = level.game.load_resource(f"{GRAPHICS_PATH}/scene_backgrounds/bg_2/{level_property['__value']}{BACKGROUND_IMAGE_FILE_EXTENSION}")
                            
                            if os.path.exists(bg_image_path):
                                level.bg_2 = {}
                                level.bg_2["parallax_x"] = 0.1
                                level.bg_2["parallax_y"] = 0.5
                                level.bg_2["image"] = pygame.image.load(bg_image_path)
                

                            bg_image_path = level.game.load_resource(f"{GRAPHICS_PATH}/scene_backgrounds/bg_3/{level_property['__value']}{BACKGROUND_IMAGE_FILE_EXTENSION}")
                            
                            if os.path.exists(bg_image_path):
                                level.bg_3 = {}
                                level.bg_3["parallax_x"] = 0.3
                                level.bg_3["parallax_y"] = 0.75
                                level.bg_3["image"] = pygame.image.load(bg_image_path)
                    
                    level.camera.set_bounds(0, level.width, 0, level.height)



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
        