import pygame
from src.state import State
from src.menu import Menu
from src.screens.settingsscreen.resources import *
from settings import *


class SelectSetting(State):
    def on_state_enter(self, settings_screen):
        settings_screen.set_heading_text(HEADING_TEXT)

        # settings_screen.game.play_sound(SELECT_A_FILE_FX)   
           
        self.current_menu_selection = "display"

        self.menu_font = pygame.font.Font(settings_screen.game.load_resource(MENU_SELECTION_FONT),file_info_font_size)

        self.menu = Menu("settings", "display")
        

    def process_events(self, settings_screen):            
        if settings_screen.game.is_button_released(DOWN_BUTTON):
            self.menu.get_next_menu_item()
            settings_screen.game.play_sound(MENU_SELECT_SOUND)

        if settings_screen.game.is_button_released(UP_BUTTON):
            self.menu.get_previous_menu_item()
            settings_screen.game.play_sound(MENU_SELECT_SOUND)

        if settings_screen.game.is_button_released(START_BUTTON) or settings_screen.game.is_button_released(ACTION_BUTTON_1):
            if self.menu.get_current_selection() == "back":
                settings_screen.game.play_sound(BACK_FX)
                settings_screen.go_to_title_screen()
                

    def draw(self, settings_screen):
        self.menu.draw_menu( 
                  self.menu_font, 
                  MENU_SELECTION_COLOR,
                  settings_screen.game.get_screen(),
                  settings_screen.grow_factor,
                  True)
