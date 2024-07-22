import pygame
from src.state import State
from src.screens.fileselectscreen.resources import *  
from src.menu import Menu, FileSelectMenu
from src.bob import bob


class SelectFile(State):
    def on_state_enter(self, file_select_screen):

        file_select_screen.set_select_a_file_text(SELECT_A_FILE_TEXT)

        bob.play_sound(SELECT_A_FILE_FX)

        self.menu_y_start_position = 72        
        self.current_menu_selection = "file_1"

        self.file_info_font = pygame.font.Font(file_select_screen.game.load_resource(menu_selection_font_path),file_info_font_size)

        self.menu = FileSelectMenu("select_file", "file_1")
        
        
        save_files = [FILE_1_NAME, FILE_2_NAME, FILE_3_NAME]
        index = 0
        for file_name in save_files:
            filepath = file_name
            if file_name in file_select_screen.game._save_file_database:
                if "last_saved" in file_select_screen.game._save_file_database[file_name]:
                    last_saved = file_select_screen.game._save_file_database[file_name]["last_saved"]
                    self.menu.set_menu_element(index, "last_saved", last_saved)
                if "percent_to_plan" in file_select_screen.game._save_file_database[file_name]:
                    percent_to_plan = file_select_screen.game._save_file_database[file_name]["percent_to_plan"]
                    self.menu.set_menu_element(index, "percent_to_plan", percent_to_plan)
            index +=1

    
    def process_events(self, file_select_screen):            
        if file_select_screen.game.is_button_released(DOWN_BUTTON):
                self.menu.get_next_menu_item()
                bob.play_sound(file_select_screen_menu_select_sound_path)

        if file_select_screen.game.is_button_released(UP_BUTTON):
            self.menu.get_previous_menu_item()
            bob.play_sound(file_select_screen_menu_select_sound_path)

        if file_select_screen.game.is_button_released(START_BUTTON) or file_select_screen.game.is_button_released(ACTION_BUTTON_1):
            if self.menu.get_current_selection() == "back":
                file_select_screen.game.play_sound(BACK_FX)
                file_select_screen.state.set_state(file_select_screen, "go_to_title_screen")
            if self.menu.get_current_selection() == "erase":
                file_select_screen.game.play_sound(MENU_OPEN_SOUND)
                file_select_screen.erase_file()
            if self.menu.get_current_selection() == "copy":
                file_select_screen.game.play_sound(MENU_OPEN_SOUND)
                file_select_screen.select_source_file()

            if self.current_menu_selection == "file_1" or "file_2" or "file_3":
                for menu_item in self.menu.get_menu():
                    if "file_name" in menu_item:
                        if menu_item["name"] == self.menu.get_current_selection():
                            filepath = menu_item['file_name']

                            file_select_screen.game.set_current_save_file(filepath)

                            if menu_item["last_saved"] == "EMPTY":
                                file_select_screen.game.create_new_save_file(filepath)

                                file_select_screen.game.play_sound(ITS_BOBBY_TIME_FX)
                                file_select_screen.game.stop_music()
                                file_select_screen.start_new_game()
                            else:
                                file_select_screen.game.load_save_file(filepath)
                                file_select_screen.game.play_sound(ITS_BOBBY_TIME_FX)
                                file_select_screen.game.stop_music()
                                file_select_screen.load_saved_game()

    def draw(self, file_select_screen):
        self.menu.draw_menu(
                  self.file_info_font, 
                  menu_selection_text_color,
                  file_select_screen.game.get_screen(),
                  file_select_screen.grow_factor,
                  True)