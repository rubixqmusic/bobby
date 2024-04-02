import logging
import pygame
import math

from res.settings import *
from res.framework.state import State
from res.framework.camera import Camera
from res.framework.animatedsprite import AnimatedSprite

TRANSITION_SPRITESHEET = f"{GRAPHICS_PATH}/screen_transitions/screen_transitions.png"
TRANSITION_ANIMATION = f"{ANIMATIONS_PATH}/screen_transitions.json"

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
        self.bg_color = None
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

        self.load_scene(self.level_name, self.player_start_position, None, "money_in")

    def process_events(self, game):
        if game.game_should_quit():
            game.quit_game()
        # self.state.process_events(self)
    
    def update(self, game):
        self.state.update(self)

    def draw(self, game):
        game.get_screen().fill(f"#0000DD")
        self.state.draw(self)

    def pause(self):
        self.paused = True
    
    def unpause(self):
        self.paused = False

    def load_scene(self, level_name, player_start_position, transition_out=None, transition_in=None):
        self.level_name = level_name,
        self.player_start_position = player_start_position
        self.transition_out = transition_out
        self.transition_in = transition_in

        if self.transition_out == None:
            self.state.set_state(self,"load_scene", self.level_name, self.player_start_position, self.transition_in)
    
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
    ...

level_states = {
                "load_scene" : LoadScene,
                "money_in_transition" : MoneyInTransition,
                "level_active" : LevelActive
                }
        