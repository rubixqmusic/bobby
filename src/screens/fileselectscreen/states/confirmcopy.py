import pygame
from src.state import State
from src.screens.fileselectscreen.resources import *  
from src.menu import Menu

class ConfirmCopy(State):
    def on_state_enter(self, file_select_screen):

        file_select_screen.set_select_a_file_text(ARE_YOU_SURE_TEXT)

        file_select_screen.game.play_sound(MENU_OPEN_SOUND)

        self.menu_y_start_position = 72        
        self.current_menu_selection = "no"

        self.file_info_font = pygame.font.Font(file_select_screen.game.load_resource(menu_selection_font_path),FILE_CONFIRM_FONT_SIZE)

        self.menu = Menu("confirm_copy", "no")
        

    
    def process_events(self, file_select_screen):            
        if file_select_screen.game.is_button_released(DOWN_BUTTON):
                self.menu.get_next_menu_item()
                file_select_screen.game.play_sound(file_select_screen_menu_select_sound_path)

        if file_select_screen.game.is_button_released(UP_BUTTON):
            self.menu.get_previous_menu_item()
            file_select_screen.game.play_sound(file_select_screen_menu_select_sound_path)

        if file_select_screen.game.is_button_released(START_BUTTON) or file_select_screen.game.is_button_released(ACTION_BUTTON_1):
            if self.menu.get_current_selection() == "no":
                file_select_screen.game.play_sound(BACK_FX)
                file_select_screen.select_file()
            
            if self.menu.get_current_selection() == "yes":
                file_select_screen.game.play_sound(BACK_FX)
                file_select_screen.game.copy_save_file(file_select_screen.source_file, file_select_screen.destination_file)
                # file_select_screen.game.save_game()
                file_select_screen.file_copied()


    def draw(self, file_select_screen):
        self.menu.draw_menu( 
                  self.file_info_font, 
                  menu_selection_text_color,
                  file_select_screen.game.get_screen(),
                  file_select_screen.grow_factor,
                  True)