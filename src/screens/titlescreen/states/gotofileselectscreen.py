import pygame
from src.state import State

class GoToFileSelectScreen(State):
    def on_state_enter(self, title_screen):
        self.min_fade = 0
        self.max_fade = 255
        self.fade = self.max_fade
        self.fade_step = 5
    
    def draw(self, title_screen):
        if self.fade > self.min_fade:
            title_screen.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
            self.fade -= self.fade_step
        else:
            self.fade = 0
            title_screen.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
            title_screen.game.load_file_select_screen()