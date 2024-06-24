import pygame
from src.menus import menus

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