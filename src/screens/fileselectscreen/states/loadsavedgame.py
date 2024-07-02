import pygame
from src.state import State

class LoadSavedGame(State):
    def on_state_enter(self, file_select_screen):
        
        self.min_fade = 0
        self.max_fade = 255
        self.fade = self.max_fade
        self.fade_step = 5
        self.hold = 60
        self.step = 1
    
    def draw(self, file_select_screen):
        if self.step ==1:
            if self.fade > self.min_fade:
                file_select_screen.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
                self.fade -= self.fade_step
            else:
                self.step = 2

        if self.step ==2:
            self.fade = 0
            file_select_screen.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
            if self.hold > 0:
                self.hold -= 1
            else:
                file_select_screen.game.load_world_map()