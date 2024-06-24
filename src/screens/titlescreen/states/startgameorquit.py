import pygame
from src.state import State
from src.menu import Menu
from settings import *
from src.screens.titlescreen.resources import *

class StartGameOrQuit(State):
    def on_state_enter(self, title_screen): 
        self.menu = Menu("title_screen", "start_game")
    
    def process_events(self, title_screen):            
        if title_screen.game.is_button_released(DOWN_BUTTON):
                self.menu.get_next_menu_item()
                title_screen.game.play_sound(title_screen_menu_select_sound_path)

        if title_screen.game.is_button_released(UP_BUTTON):
            self.menu.get_previous_menu_item()
            title_screen.game.play_sound(title_screen_menu_select_sound_path)

        if title_screen.game.is_button_released(START_BUTTON):
            if self.menu.get_current_selection() == "start_game":
                title_screen.game.play_sound(LETS_GO_FX)
                title_screen.go_to_file_select_screen()

            if self.menu.get_current_selection() == "settings":
                title_screen.game.play_sound(LETS_GO_FX)
                title_screen.go_to_settings_screen()

            if self.menu.get_current_selection() == "quit_game":
                title_screen.game.play_sound(FUCK_YOU_FX)
                title_screen.game.stop_music()
                title_screen.fade_out_and_quit()

    def draw(self, title_screen):
        self.menu.draw_menu(
                  title_screen.menu_selection_font, 
                  menu_selection_text_color,
                  title_screen.game.get_screen(),
                  title_screen.grow_factor,
                  True)