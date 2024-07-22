import pygame
from src.state import State

class ReturnToWorldMap(State):
    def on_state_enter(self, gameplay):
        self.min_fade = 0
        self.max_fade = 255
        self.fade = self.max_fade
        self.fade_step = 5
    
    def draw(self, gameplay):
        if self.fade > self.min_fade:
            gameplay.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
            self.fade -= self.fade_step
        else:
            self.fade = 0
            gameplay.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
            gameplay.game.load_world_map()