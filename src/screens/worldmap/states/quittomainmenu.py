import pygame
from src.state import State

class QuitToMainMenu(State):
    def on_state_enter(self, world_map):
        self.min_fade = 0
        self.max_fade = 255
        self.fade = self.max_fade
        self.fade_step = 5
    
    def draw(self, world_map):
        if self.fade > self.min_fade:
            world_map.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
            self.fade -= self.fade_step
        else:
            self.fade = 0
            world_map.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
            world_map.game.load_title_screen()