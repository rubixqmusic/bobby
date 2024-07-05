import pygame
from src.state import State
from src.screens.worldmap.resources import *

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
            world_map.map_active()