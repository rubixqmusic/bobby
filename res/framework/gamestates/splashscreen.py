import logging
import pygame

from res.settings import *
from res.framework.state import State

class Splashscreen(State):   
    def on_state_enter(self, game):
        logging.debug(f"loaded splashscreen state")
        self.text = "Kablio"
        self.font_size = 32
        self.font_color = f"#fbcb1d"
        self.text_font = pygame.font.Font(game.load_resource(f"{FONTS_PATH}/{DEFAULT_FONT}"), self.font_size)
        self.text_surface = self.text_font.render(self.text, False, self.font_color, None)

        self.min_fade = 0
        self.max_fade = 255
        self.fade = self.max_fade
        self.fade_step = 10

        self.event_step = 0

        self.event_timer = 60

    def process_events(self, game):
        ...
    
    def draw(self, game):
        game.get_screen().fill(f"#000000")

        if self.event_step == 0:
            if self.event_timer >= 0:
                self.event_timer -=1
            else:
                self.event_timer = 100
                self.event_step = 1
        
        if self.event_step == 1:
            game.play_sound(game.load_resource(f"{SOUNDS_PATH}/coin.wav"))
            self.event_step = 2
        
        if self.event_step == 2:
            if self.event_timer >= 0:
                text_rect = self.text_surface.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
                game.get_screen().blit(self.text_surface, text_rect)
                self.event_timer -= 1
            else:
                self.event_timer = 100
                self.event_step = 3
        
        if self.event_step == 3:
            if self.fade > self.max_fade:
                self.fade = self.max_fade
            if self.fade > self.min_fade:
                text_rect = self.text_surface.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
                game.get_screen().blit(self.text_surface, text_rect)
                game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
                self.fade -= self.fade_step
            else:
                self.event_step = 4
                self.event_timer = 200
        
        if self.event_step == 4:
            self.event_timer -= 1
            if self.event_timer < 0:
                game.state.set_state(game,"title_screen")
        
        