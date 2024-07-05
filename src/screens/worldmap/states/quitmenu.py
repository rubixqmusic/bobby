import pygame

from src.state import State
from src.menu import Menu
from src.screens.worldmap.resources import *

class QuitMenu(State):
    def on_state_enter(self, world_map):
        self.menu_box_surface = pygame.image.load(world_map.game.load_resource(QUIT_MENU_IMAGE))
        self.menu_box_rect = self.menu_box_surface.get_rect()
        self.menu_box_width = self.menu_box_surface.get_width()
        self.max_menu_box_y = self.menu_box_surface.get_height()
        self.min_menu_box_size = 1
        self.menu_box_step_size = 10
        self.menu_box_step = 0

        self.current_menu_selection = "continue"

        self.menu = Menu("world_map_quit_menu", "continue")
        
        self.set_status("open_menu")
        world_map.game.play_sound(MENU_OPEN_SOUND)

    def update(self, world_map):
        if self.status == "open_menu":
            self.open_menu()

        elif self.status == "menu_active":
            if world_map.game.is_button_released(SELECT_BUTTON):
                self.set_status("close_menu")
                world_map.game.play_sound(MENU_CLOSE_SOUND)
            
            if world_map.game.is_button_released(DOWN_BUTTON):
                self.menu.get_next_menu_item()
                world_map.game.play_sound(QUIT_MENU_SELECT_SOUND)
            if world_map.game.is_button_released(UP_BUTTON):
                self.menu.get_previous_menu_item()
                world_map.game.play_sound(QUIT_MENU_SELECT_SOUND)

            if world_map.game.is_button_released(START_BUTTON) or world_map.game.is_button_released(ACTION_BUTTON_1):
                if self.menu.get_current_selection() == "continue":
                    self.set_status("close_menu")
                    world_map.game.play_sound(MENU_CLOSE_SOUND)
                elif self.menu.get_current_selection() == "return_to_main_menu":
                    world_map.quit_to_main_menu()
                    world_map.game.play_sound(RETURN_TO_MAIN_MENU_SOUND)
                    world_map.game.stop_music()
            

        elif self.status == "close_menu":
            self.close_menu()
                # world_map.map_active()
        elif self.status == "return_to_map":
            world_map.map_active()
    

    def draw(self, world_map):
        if self.status == "open_menu":
            scaled_menu_image = pygame.transform.scale(self.menu_box_surface, [self.menu_box_width, self.menu_box_step])
            menu_rect = scaled_menu_image.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
            world_map.game.get_screen().blit(scaled_menu_image, menu_rect)
        
        if self.status == "menu_active":
            # scaled_menu_image = pygame.transform.scale(self.menu_box_surface, [self.menu_box_width, self.menu_box_step])
            menu_rect = self.menu_box_surface.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
            world_map.game.get_screen().blit(self.menu_box_surface, menu_rect)
            self.menu.draw_menu(world_map.font, world_map.font_color, world_map.game.get_screen(),world_map.grow_factor)

        if self.status == "close_menu":
            scaled_menu_image = pygame.transform.scale(self.menu_box_surface, [self.menu_box_width, self.menu_box_step])
            menu_rect = scaled_menu_image.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
            world_map.game.get_screen().blit(scaled_menu_image, menu_rect)

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