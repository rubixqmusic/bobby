import pygame
from src.state import State
from src.screens.initscreen.resources import *

class ControlNotification(State):
    def on_state_enter(self, init_screen):
        self.regular_font = pygame.font.Font(init_screen.game.load_resource(f"{FONTS_PATH}/{DEFAULT_FONT}"), REGULAR_FONT_SIZE)
        self.large_font = pygame.font.Font(init_screen.game.load_resource(f"{FONTS_PATH}/{DEFAULT_FONT}"), LARGE_FONT_SIZE)

        self.control_info_text = self.regular_font.render(CONTROL_INFO_TEXT, True, FONT_COLOR)
        self.quit_info_text = self.regular_font.render(QUIT_INFO_TEXT, True, FONT_COLOR)
        self.press_enter_text = self.large_font.render(PRESS_ENTER_TEXT, True, FONT_COLOR)

        self.control_info_rect = self.control_info_text.get_rect(center=(SCREEN_WIDTH/2, 40))
        self.quit_info_rect = self.quit_info_text.get_rect(center=(SCREEN_WIDTH/2, 60))
        self.press_enter_rect = self.press_enter_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    
    def update(self, init_screen):
        if init_screen.game.is_button_released(START_BUTTON):
            init_screen.load_splashscreen()

    def draw(self, init_screen):
        init_screen.game.get_screen().fill((0,0,0))
        init_screen.game.get_screen().blit(self.control_info_text, self.control_info_rect)
        init_screen.game.get_screen().blit(self.quit_info_text, self.quit_info_rect)
        init_screen.game.get_screen().blit(self.press_enter_text, self.press_enter_rect)