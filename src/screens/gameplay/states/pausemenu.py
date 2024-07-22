import pygame

from src.state import State
from src.menu import Menu
from src.screens.gameplay.resources import *

class PauseMenu(State):
    def on_state_enter(self, gameplay):
        gameplay.pause()
        self.menu_box_surface = pygame.image.load(gameplay.game.load_resource(PAUSE_MENU_IMAGE))
        self.menu_box_rect = self.menu_box_surface.get_rect()
        self.menu_box_width = self.menu_box_surface.get_width()
        self.max_menu_box_y = self.menu_box_surface.get_height()
        self.min_menu_box_size = 1
        self.menu_box_step_size = 10
        self.menu_box_step = 0

        self.current_menu_selection = "continue"

        self.menu = Menu("gameplay_pause_menu", "continue")
        
        self.set_status("open_menu")
        gameplay.game.play_sound(MENU_OPEN_SOUND)

    def update(self, gameplay):
        if self.status == "open_menu":
            self.open_menu()

        elif self.status == "menu_active":
            if gameplay.game.is_button_released(SELECT_BUTTON):
                self.set_status("close_menu")
                gameplay.game.play_sound(MENU_CLOSE_SOUND)
            
            if gameplay.game.is_button_released(DOWN_BUTTON):
                self.menu.get_next_menu_item()
                gameplay.game.play_sound(PAUSE_MENU_SELECT_SOUND)
            if gameplay.game.is_button_released(UP_BUTTON):
                self.menu.get_previous_menu_item()
                gameplay.game.play_sound(PAUSE_MENU_SELECT_SOUND)

            if gameplay.game.is_button_released(START_BUTTON) or gameplay.game.is_button_released(ACTION_BUTTON_1):
                if self.menu.get_current_selection() == "continue":
                    self.set_status("close_menu")
                    gameplay.game.play_sound(MENU_CLOSE_SOUND)
                elif self.menu.get_current_selection() == "return_to_title_screen":
                    gameplay.return_to_title_screen()
                    gameplay.game.play_sound(RETURN_TO_MAIN_MENU_SOUND)
                    gameplay.game.stop_music()
                elif self.menu.get_current_selection() == "return_to_world_map":
                    gameplay.return_to_world_map()
                    gameplay.game.play_sound(RETURN_TO_MAIN_MENU_SOUND)
                    gameplay.game.stop_music()
            

        elif self.status == "close_menu":
            self.close_menu()
                # gameplay.map_active()
        elif self.status == "return_to_map":
            gameplay.level_active()
            gameplay.unpause()
    

    def draw(self, gameplay):
        if self.status == "open_menu":
            scaled_menu_image = pygame.transform.scale(self.menu_box_surface, [self.menu_box_width, self.menu_box_step])
            menu_rect = scaled_menu_image.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
            gameplay.game.get_screen().blit(scaled_menu_image, menu_rect)
        
        if self.status == "menu_active":
            # scaled_menu_image = pygame.transform.scale(self.menu_box_surface, [self.menu_box_width, self.menu_box_step])
            menu_rect = self.menu_box_surface.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
            gameplay.game.get_screen().blit(self.menu_box_surface, menu_rect)
            self.menu.draw_menu(gameplay.font, PAUSE_MENU_FONT_COLOR, gameplay.game.get_screen(),gameplay.text_grow_factor)

        if self.status == "close_menu":
            scaled_menu_image = pygame.transform.scale(self.menu_box_surface, [self.menu_box_width, self.menu_box_step])
            menu_rect = scaled_menu_image.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
            gameplay.game.get_screen().blit(scaled_menu_image, menu_rect)

    def set_status(self, status):
        self.status = status

    def open_menu(self):
        self.menu_box_step += self.menu_box_step_size
        if self.menu_box_step > self.max_menu_box_y:
            self.menu_box_step = self.max_menu_box_y
            self.set_status("menu_active")
    
    def close_menu(self):
        self.menu_box_step -= self.menu_box_step_size
        if self.menu_box_step < 1:
            self.menu_box_step = 1
            self.set_status("return_to_map")