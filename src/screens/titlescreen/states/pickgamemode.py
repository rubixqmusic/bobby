import pygame

from src.screens.titlescreen.resources import *
from src.state import State
from src.menu import Menu

# from settings import *


class PickGameMode(State):
    def on_state_enter(self, title_screen):     
        self.menu = Menu("pick_game_mode", "story_mode")
    
    def process_events(self, title_screen):
            if title_screen.game.is_button_released(DOWN_BUTTON):
                self.menu.get_next_menu_item()
                title_screen.game.play_sound(title_screen_menu_select_sound_path)

            if title_screen.game.is_button_released(UP_BUTTON):
                self.menu.get_previous_menu_item()
                title_screen.game.play_sound(title_screen_menu_select_sound_path)

            if title_screen.game.is_button_released(START_BUTTON) or title_screen.game.is_button_released(ACTION_BUTTON_1):
                if self.menu.get_current_selection() == "back":
                    title_screen.game.play_sound(BACK_FX)
                    title_screen.start_game_or_quit()

            if title_screen.game.is_button_released(START_BUTTON) or title_screen.game.is_button_released(ACTION_BUTTON_1):
                if self.menu.get_current_selection() == "story_mode":
                    title_screen.game.play_sound(STORY_MODE_FX)
                    title_screen.go_to_file_select_screen()
    
    def draw(self, title_screen):
        self.menu.draw_menu(
                title_screen.menu_selection_font, 
                  menu_selection_text_color,
                  title_screen.game.get_screen(),
                  title_screen.grow_factor,
                  True)