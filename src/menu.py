import pygame
from src.menus.menus import *
from src.bob import bob

class Menu:
    def __init__(self, menu_name, initial_selection) -> None:

        if menu_name in menus:
            self._menu = menus[menu_name]
        else:
            self._menu = None

        self._current_selection = initial_selection

        if self._menu:
            index = 0
            for menu_item in self._menu:
                if menu_item["name"] == self._current_selection:
                    self._current_selection = self._menu[index]["name"]
                    break
                index += 1
                if index > len(self._menu) - 1:
                    index = 0
                    self._current_selection = self._menu[index]["name"]
                    

    def draw_menu(self,
              font: pygame.font.Font, 
              font_color: str, 
              destination_surface: pygame.surface.Surface, 
              grow_factor: int,
              drop_shadow=False,
              drop_shadow_color=f"#000000",
              drop_shadow_x=1,
              drop_shadow_y=1):
    
        if not self._menu:
            return
        
        menu_item_index = 0
        for menu_item in self._menu:
            text_surface = font.render(menu_item['text'],True,font_color)
            text_surface_base_size = text_surface.get_width(), text_surface.get_height()
            drop_shadow_surface = None
            if drop_shadow:
                drop_shadow_surface = font.render(menu_item['text'],True,drop_shadow_color)
            
            if menu_item["name"] == self._current_selection:
                if drop_shadow_surface is not None:
                    drop_shadow_surface_new = pygame.transform.scale(drop_shadow_surface, 
                                        (text_surface_base_size[0] + grow_factor, 
                                        text_surface_base_size[1] + grow_factor))
                    drop_shadow_rect = drop_shadow_surface_new.get_rect(center=(menu_item["position"][0] + drop_shadow_x, menu_item["position"][1]+drop_shadow_y))
                    destination_surface.blit(drop_shadow_surface, drop_shadow_rect)
                
                new_surface = pygame.transform.scale(text_surface, 
                                        (text_surface_base_size[0] + grow_factor, 
                                        text_surface_base_size[1] + grow_factor))
                text_rect = new_surface.get_rect(center=(menu_item["position"]))
                destination_surface.blit(new_surface, text_rect)
            else:
                if drop_shadow_surface is not None:
                    drop_shadow_rect = drop_shadow_surface.get_rect(center=(menu_item["position"][0] + drop_shadow_x, menu_item["position"][1]+drop_shadow_y))
                    destination_surface.blit(drop_shadow_surface, drop_shadow_rect)
                text_rect = text_surface.get_rect(center=(menu_item["position"]))
                destination_surface.blit(text_surface, text_rect)
        
            menu_item_index += 1
    
    def get_next_menu_item(self):
        if not self._menu:
            return
        
        index = 0
        for menu_item in self._menu:

            if menu_item["name"] == self._current_selection:
                index += 1
                if index > len(self._menu) - 1:
                    index = 0
                self._current_selection = self._menu[index]["name"]
                return
            index += 1

    def get_previous_menu_item(self,):
        if not self._menu:
            return
        
        index = 0
        for menu_item in self._menu:

            if menu_item["name"] == self._current_selection:
                index -= 1
                if index < 0:
                    index = len(self._menu) - 1
                self._current_selection = self._menu[index]["name"]
                return
            index += 1
    
    def get_current_selection(self):
        return self._current_selection
    
    def get_menu(self):
        return self._menu
    
    def set_menu_element(self, index, menu_element, new_value):
        if index >= 0 and index <= len(self._menu) -1:

            if menu_element in self._menu[index]:
                self._menu[index][menu_element] = new_value



class FileSelectMenu(Menu):
    def draw_menu(self, 
                  font: pygame.Font, 
                  font_color: str, 
                  destination_surface: pygame.Surface, 
                  grow_factor: int, 
                  drop_shadow=False, 
                  drop_shadow_color=f"#000000", 
                  drop_shadow_x=1, 
                  drop_shadow_y=1):
        
        Y_TEXT_POSITION = 28
        FILE_NUMBER_X_POSITION = 6
        LAST_PLAYED_X_POSITION = 19
        PERCENT_X_POSITION = 105
        
        if not self._menu:
            return
        
        menu_item_index = 0
        for menu_item in self._menu:
            if "bg_image" in menu_item:
                file_info_background = pygame.image.load(bob.load_resource(FILE_SELECT_BACKGROUND))
                file_number_text_surface = font.render(str(menu_item_index+1),True,(0,0,0))
                last_played_text_surface = font.render(menu_item['last_saved'],True,(0,0,0))
                percent_text_surface = font.render(menu_item['percent_to_plan'],True,(0,0,0))

                file_number_rect = file_number_text_surface.get_rect(center=(file_number_text_surface.get_rect().x + FILE_NUMBER_X_POSITION, Y_TEXT_POSITION))
                last_played_rect = file_number_text_surface.get_rect(center=(file_number_text_surface.get_rect().x + LAST_PLAYED_X_POSITION, Y_TEXT_POSITION))
                percent_rect = file_number_text_surface.get_rect(center=(file_number_text_surface.get_rect().x + PERCENT_X_POSITION, Y_TEXT_POSITION))
                file_info_background.blit(file_number_text_surface,file_number_rect)
                file_info_background.blit(last_played_text_surface,last_played_rect)
                file_info_background.blit(percent_text_surface,percent_rect)

                file_info_base_size = file_info_background.get_width(), file_info_background.get_height()

                if menu_item["name"] == self.get_current_selection():
                    new_surface = pygame.transform.scale(file_info_background, (file_info_base_size[0] + grow_factor, file_info_base_size[1]+grow_factor))

                    file_info_rect = new_surface.get_rect(center=(menu_item["position"]))
                    destination_surface.blit(new_surface, file_info_rect)
                else:
                    file_info_rect = file_info_background.get_rect(center=(menu_item["position"]))
                    destination_surface.blit(file_info_background, file_info_rect)

            else:
                text_surface = font.render(menu_item['text'],True,font_color)
                text_surface_base_size = text_surface.get_width(), text_surface.get_height()
                drop_shadow_surface = None
                if drop_shadow:
                    drop_shadow_surface = font.render(menu_item['text'],True,drop_shadow_color)
                
                if menu_item["name"] == self._current_selection:
                    if drop_shadow_surface is not None:
                        drop_shadow_surface_new = pygame.transform.scale(drop_shadow_surface, 
                                            (text_surface_base_size[0] + grow_factor, 
                                            text_surface_base_size[1] + grow_factor))
                        drop_shadow_rect = drop_shadow_surface_new.get_rect(center=(menu_item["position"][0] + drop_shadow_x, menu_item["position"][1]+drop_shadow_y))
                        destination_surface.blit(drop_shadow_surface, drop_shadow_rect)
                    
                    new_surface = pygame.transform.scale(text_surface, 
                                            (text_surface_base_size[0] + grow_factor, 
                                            text_surface_base_size[1] + grow_factor))
                    text_rect = new_surface.get_rect(center=(menu_item["position"]))
                    destination_surface.blit(new_surface, text_rect)
                else:
                    if drop_shadow_surface is not None:
                        drop_shadow_rect = drop_shadow_surface.get_rect(center=(menu_item["position"][0] + drop_shadow_x, menu_item["position"][1]+drop_shadow_y))
                        destination_surface.blit(drop_shadow_surface, drop_shadow_rect)
                    text_rect = text_surface.get_rect(center=(menu_item["position"]))
                    destination_surface.blit(text_surface, text_rect)
        
            menu_item_index += 1
