import pygame
from src.state import State

class FadeIn(State):
    def on_state_enter(self, title_screen):
        self.min_fade = 0
        self.max_fade = 255
        self.fade = self.min_fade
        self.fade_step = 5
    
    def draw(self, title_screen):
        if self.fade < self.max_fade:
            title_screen.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
            self.fade += self.fade_step
        else:
            title_screen.start_game_or_quit()