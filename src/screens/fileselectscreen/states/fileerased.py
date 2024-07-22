import pygame
from src.state import State
from src.screens.fileselectscreen.resources import *

class FileErased(State):
    def on_state_enter(self, file_select_screen):
        file_select_screen.set_select_a_file_text(FILE_ERASED_TEXT)

    def process_events(self, file_select_screen):            
        if file_select_screen.game.is_button_released(START_BUTTON) or file_select_screen.game.is_button_released(ACTION_BUTTON_1):
            # file_select_screen.game.play_sound(BACK_FX)
            file_select_screen.select_file()