import logging
import pygame

from res.settings import *
from res.framework.state import State

WORLD_MAP_MUSIC = f"{MUSIC_PATH}/world_map.mp3"
BACKGROUND_IMAGE = f"{GRAPHICS_PATH}/backgrounds/world_map_background.png"
MAP_BOX = f"{GRAPHICS_PATH}/backgrounds/world_map_box.png"



class WorldMap(State):
    def on_state_enter(self, game):

        self.game = game
        
        self.background_image = pygame.image.load(game.load_resource(BACKGROUND_IMAGE)).convert_alpha()
        self.map_box = pygame.image.load(game.load_resource(MAP_BOX)).convert_alpha()

        game.play_music(game.load_resource(WORLD_MAP_MUSIC))

        self.state = State(world_map_states)
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
            # world_map.state.set_state(world_map, "start_game_or_quit")
            piss = 0

world_map_states = {
            "fade_in" : FadeIn
}