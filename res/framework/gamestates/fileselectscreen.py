import logging
import pygame
import math
import os
import json

from res.settings import *
from res.framework.state import State

# SAVE_DATA_PATH = f"{os.path.expanduser('~')}/.bobby"
NEW_GAME_CUTSCENE_NAME = f"intro_1"

background_image_path = f"{GRAPHICS_PATH}/backgrounds/title_screen_background.png"
trees_image_path = f"{GRAPHICS_PATH}/backgrounds/title_screen_trees.png"
file_select_screen_music_path = f"{MUSIC_PATH}/title_screen.mp3"
file_select_background_path = f"{GRAPHICS_PATH}/backgrounds/file_select_background.png"
# file_select_screen_text_path = f"{GRAPHICS_PATH}/backgrounds/file_select_screen_text.png"
file_select_screen_menu_select_sound_path = f"{SOUNDS_PATH}/menu_select.wav"
file_select_screen_menu_select_sound_volume = 0.7
coin_sound_path = f"{SOUNDS_PATH}/coin.wav"

BACK_FX = f"{SOUNDS_PATH}/video_call_decline.wav"

SELECT_A_FILE_FX = f"{SOUNDS_PATH}/select_a_file.wav"
ITS_BOBBY_TIME_FX = f"{SOUNDS_PATH}/its_bobby_time.wav"

# scroll_speed = 1

menu_selection_font_path = f"{FONTS_PATH}/{DEFAULT_FONT}"
menu_selection_text_size = 16
select_a_file_font_size = 20
main_text_color = f"#fbcb1d"
menu_selection_text_color = f"#fe112b"
menu_drop_shadow_x = 1
menu_drop_shadow_y = 1
menu_drop_shadow_color = f"#000000"

select_a_file_text = f"Select A File"
select_a_file_text_y_position = 32

file_info_font_size = 10

text_y_spacing = 60
max_text_grow = 5.0
text_grow_step_size = 0.1
sine_degrees = 0.0
grow_factor = 0

# FILE_1_NAME = "file_1.json"
# FILE_2_NAME = "file_2.json"
# FILE_3_NAME = "file_3.json"


class FileSelectScreen(State):
    def on_state_enter(self, game):
        # if not os.path.exists(SAVE_DATA_PATH):
        #     try:
        #         os.mkdir(SAVE_DATA_PATH)
        #     except:
        #         logging.debug(f"Could not create save data path {SAVE_DATA_PATH}, make sure you have proper privileges to create this file!")
        
        # save_files = [FILE_1_NAME, FILE_2_NAME, FILE_3_NAME]

        # for file_name in save_files:
        #     filepath = f"{SAVE_DATA_PATH}/{file_name}"
        #     if os.path.exists(filepath):
        #         with open(filepath) as save_file:
        #             save_file_data = json.load(save_file)

        #             # load in the data you need to the file info images menu

        self.sine_degrees = 0
        self.grow_factor = 0
        self.game = game
        self.background_image = pygame.image.load(self.game.load_resource(background_image_path)).convert_alpha()
        '''use this to dim the background image'''
        self.background_image.set_alpha(100)

        self.trees_image = pygame.image.load(self.game.load_resource(trees_image_path)).convert_alpha()
        self.trees_image_wrap = pygame.image.load(self.game.load_resource(trees_image_path)).convert_alpha()
        self.trees_image_position = [0,0]

        self.menu_selection_font = pygame.font.Font(game.load_resource(menu_selection_font_path),menu_selection_text_size)

        self.select_a_file_font = pygame.font.Font(game.load_resource(menu_selection_font_path), select_a_file_font_size)
        self.select_a_file_text_surface = self.select_a_file_font.render(select_a_file_text,True,main_text_color)

        game.play_music(file_select_screen_music_path)
        
        
        self.state = State(file_select_screen_states)
        self.state.start(self, "fade_in")

    def process_events(self, game):
        if game.game_should_quit():
            game.quit_game()

        self.state.process_events(self)

    def update(self, game):
        self.grow_factor = int(math.sin(self.sine_degrees) * max_text_grow)
        self.sine_degrees += text_grow_step_size%max_text_grow

        self.state.update(self)

    def draw(self, game):
        text_rect = self.select_a_file_text_surface.get_rect(center=(SCREEN_WIDTH/2, select_a_file_text_y_position))
        game.get_screen().fill("#000000")
        game.get_screen().blit(self.background_image, (0,0))
        game.get_screen().blit(self.trees_image, self.trees_image_position)
        game.get_screen().blit(self.select_a_file_text_surface, text_rect)
        self.state.draw(self)

    def start_new_game(self):
        self.state.set_state(self, "start_new_game")

    def load_saved_game(self):
        self.state.set_state(self, "load_saved_game")

class FadeIn(State):
    def on_state_enter(self, file_select_screen):
        self.min_fade = 0
        self.max_fade = 255
        self.fade = self.min_fade
        self.fade_step = 5
    
    def draw(self, file_select_screen):
        if self.fade < self.max_fade:
            file_select_screen.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
            self.fade += self.fade_step
        else:
            file_select_screen.state.set_state(file_select_screen, "select_file")


class GoToTitleScreen(State):
    def on_state_enter(self, file_select_screen):
        self.min_fade = 0
        self.max_fade = 255
        self.fade = self.max_fade
        self.fade_step = 5
    
    def draw(self, file_select_screen):
        if self.fade > self.min_fade:
            file_select_screen.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
            self.fade -= self.fade_step
        else:
            self.fade = 0
            file_select_screen.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
            file_select_screen.game.load_title_screen()
  

class StartNewGame(State):
    def on_state_enter(self, file_select_screen):
        
        self.min_fade = 0
        self.max_fade = 255
        self.fade = self.max_fade
        self.fade_step = 5
    
    def draw(self, file_select_screen):
        if self.fade > self.min_fade:
            file_select_screen.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
            self.fade -= self.fade_step
        else:
            self.fade = 0
            file_select_screen.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
            file_select_screen.game.run_video_call_cutscene(NEW_GAME_CUTSCENE_NAME)


class LoadSavedGame(State):
    def on_state_enter(self, file_select_screen):
        
        self.min_fade = 0
        self.max_fade = 255
        self.fade = self.max_fade
        self.fade_step = 5
        self.hold = 60
        self.step = 1
    
    def draw(self, file_select_screen):
        if self.step ==1:
            if self.fade > self.min_fade:
                file_select_screen.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
                self.fade -= self.fade_step
            else:
                self.step = 2

        if self.step ==2:
            self.fade = 0
            file_select_screen.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
            if self.hold > 0:
                self.hold -= 1
            else:
                file_select_screen.game.load_world_map()


class SelectFile(State):
    def on_state_enter(self, file_select_screen):

        file_select_screen.game.play_sound(SELECT_A_FILE_FX)

        self.menu_y_start_position = 72        
        self.current_menu_selection = "file_1"

        self.file_info_font = pygame.font.Font(file_select_screen.game.load_resource(menu_selection_font_path),file_info_font_size)

        self.menu = [
                        {"name" : "file_1", "text" : "NEW", "file_name" : FILE_1_NAME, "bg_image" : file_select_background_path, "date_created" : "", "last_saved": "EMPTY", "percent_to_plan" : "0/100"},
                        {"name" : "file_2", "text" : "NEW", "file_name" : FILE_2_NAME, "bg_image" : file_select_background_path, "date_created" : "", "last_saved": "EMPTY", "percent_to_plan" : "0/100"},
                        {"name" : "file_3", "text" : "NEW", "file_name" : FILE_3_NAME, "bg_image" : file_select_background_path, "date_created" : "", "last_saved": "EMPTY", "percent_to_plan" : "0/100"},
                        {"name" : "back", "text" : "Back"},
                        # {"name" : "copy", "text" : "Copy"},
                        # {"name" : "erase", "text" : "Erase"}
                    ]
        
        # if not os.path.exists(SAVE_DATA_PATH):
        #     try:
        #         os.mkdir(SAVE_DATA_PATH)
        #     except:
        #         logging.debug(f"Could not create save data path {SAVE_DATA_PATH}, make sure you have proper privileges to create this file!")
        
        save_files = [FILE_1_NAME, FILE_2_NAME, FILE_3_NAME]
        index = 0
        for file_name in save_files:
            filepath = f"{SAVE_DATA_PATH}/{file_name}"
            if os.path.exists(filepath):
                with open(filepath) as save_file:
                    save_file_data = json.load(save_file)
                    if "last_saved" in save_file_data:
                        self.menu[index]["last_saved"] = save_file_data["last_saved"]
                    if "percent_to_plan" in save_file_data:
                        self.menu[index]["percent_to_plan"] = save_file_data["percent_to_plan"]
            index +=1

    
    def process_events(self, file_select_screen):            
        if file_select_screen.game.is_button_released(DOWN_BUTTON):
                self.current_menu_selection = get_next_menu_item(self.menu, self.current_menu_selection)
                file_select_screen.game.play_sound(file_select_screen_menu_select_sound_path)

        if file_select_screen.game.is_button_released(UP_BUTTON):
            self.current_menu_selection = get_previous_menu_item(self.menu, self.current_menu_selection)
            file_select_screen.game.play_sound(file_select_screen_menu_select_sound_path)

        if file_select_screen.game.is_button_released(START_BUTTON):
            if self.current_menu_selection == "back":
                file_select_screen.game.play_sound(BACK_FX)
                file_select_screen.state.set_state(file_select_screen, "go_to_title_screen")

            if self.current_menu_selection == "file_1" or "file_2" or "file_3":
                for menu_item in self.menu:
                    if "file_name" in menu_item:
                        if menu_item["name"] == self.current_menu_selection:
                            filepath = f"{SAVE_DATA_PATH}/{menu_item['file_name']}"

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
        draw_file_select_menu(file_select_screen,
                  self.menu, 
                  self.current_menu_selection, 
                  self.menu_y_start_position, 
                  text_y_spacing, 
                  self.file_info_font, 
                  menu_selection_text_color,
                  file_select_screen.game.get_screen(),
                  file_select_screen.grow_factor,
                  True)


file_select_screen_states = {
                        "fade_in" : FadeIn,
                        "select_file" : SelectFile,
                        "go_to_title_screen" : GoToTitleScreen,
                        "start_new_game" : StartNewGame,
                        "load_saved_game" : LoadSavedGame
                        }

def draw_file_select_menu(
              screen,
              menu: list, 
              current_selection: str, 
              y_start: int, 
              y_spacing: int, 
              font: pygame.font.Font, 
              font_color: str, 
              destination_surface: pygame.surface.Surface, 
              grow_factor: int,
              drop_shadow=False,
              drop_shadow_color=f"#000000",
              drop_shadow_x=1,
              drop_shadow_y=1):
    
    FILE_INFO_FONT_SIZE = 12
    Y_TEXT_POSITION = 28
    FILE_NUMBER_X_POSITION = 6
    LAST_PLAYED_X_POSITION = 19
    PERCENT_X_POSITION = 105

    menu_item_index = 0
    for menu_item in menu:
        if "bg_image" in menu_item:
            file_info_background = pygame.image.load(screen.game.load_resource(file_select_background_path))
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

            if menu_item["name"] == current_selection:
                new_surface = pygame.transform.scale(file_info_background, (file_info_base_size[0] + grow_factor, file_info_base_size[1]+grow_factor))

                file_info_rect = new_surface.get_rect(center=(SCREEN_WIDTH/2, y_start + (menu_item_index*y_spacing)))
                destination_surface.blit(new_surface, file_info_rect)
            else:
                file_info_rect = file_info_background.get_rect(center=(SCREEN_WIDTH/2, y_start + (menu_item_index*y_spacing)))
                destination_surface.blit(file_info_background, file_info_rect)
        else:
            text_surface = font.render(menu_item['text'],True,font_color)
            text_surface_base_size = text_surface.get_width(), text_surface.get_height()
            drop_shadow_surface = None
            if drop_shadow:
                drop_shadow_surface = font.render(menu_item['text'],True,drop_shadow_color)
            
            if menu_item["name"] == current_selection:
                if drop_shadow_surface is not None:
                    drop_shadow_surface_new = pygame.transform.scale(drop_shadow_surface, 
                                        (text_surface_base_size[0] + grow_factor, 
                                        text_surface_base_size[1] + grow_factor))
                    drop_shadow_rect = drop_shadow_surface_new.get_rect(center=(SCREEN_WIDTH/2 + drop_shadow_x, y_start + (menu_item_index*y_spacing)+drop_shadow_y))
                    destination_surface.blit(drop_shadow_surface, drop_shadow_rect)
                
                new_surface = pygame.transform.scale(text_surface, 
                                        (text_surface_base_size[0] + grow_factor, 
                                        text_surface_base_size[1] + grow_factor))
                text_rect = new_surface.get_rect(center=(SCREEN_WIDTH/2, y_start + (menu_item_index*y_spacing)))
                destination_surface.blit(new_surface, text_rect)
            else:
                if drop_shadow_surface is not None:
                    drop_shadow_rect = drop_shadow_surface.get_rect(center=(SCREEN_WIDTH/2 + drop_shadow_x, y_start + (menu_item_index*y_spacing)+drop_shadow_y))
                    destination_surface.blit(drop_shadow_surface, drop_shadow_rect)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH/2, y_start + (menu_item_index*y_spacing)))
                destination_surface.blit(text_surface, text_rect)
    
        menu_item_index += 1

def draw_menu(menu: list, 
              current_selection: str, 
              y_start: int, 
              y_spacing: int, 
              font: pygame.font.Font, 
              font_color: str, 
              destination_surface: pygame.surface.Surface, 
              grow_factor: int,
              drop_shadow=False,
              drop_shadow_color=f"#000000",
              drop_shadow_x=1,
              drop_shadow_y=1):
    
    menu_item_index = 0
    for menu_item in menu:
        text_surface = font.render(menu_item['text'],True,font_color)
        text_surface_base_size = text_surface.get_width(), text_surface.get_height()
        drop_shadow_surface = None
        if drop_shadow:
            drop_shadow_surface = font.render(menu_item['text'],True,drop_shadow_color)
        
        if menu_item["name"] == current_selection:
            if drop_shadow_surface is not None:
                drop_shadow_surface_new = pygame.transform.scale(drop_shadow_surface, 
                                    (text_surface_base_size[0] + grow_factor, 
                                    text_surface_base_size[1] + grow_factor))
                drop_shadow_rect = drop_shadow_surface_new.get_rect(center=(SCREEN_WIDTH/2 + drop_shadow_x, y_start + (menu_item_index*y_spacing)+drop_shadow_y))
                destination_surface.blit(drop_shadow_surface, drop_shadow_rect)
            
            new_surface = pygame.transform.scale(text_surface, 
                                    (text_surface_base_size[0] + grow_factor, 
                                    text_surface_base_size[1] + grow_factor))
            text_rect = new_surface.get_rect(center=(SCREEN_WIDTH/2, y_start + (menu_item_index*y_spacing)))
            destination_surface.blit(new_surface, text_rect)
        else:
            if drop_shadow_surface is not None:
                drop_shadow_rect = drop_shadow_surface.get_rect(center=(SCREEN_WIDTH/2 + drop_shadow_x, y_start + (menu_item_index*y_spacing)+drop_shadow_y))
                destination_surface.blit(drop_shadow_surface, drop_shadow_rect)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH/2, y_start + (menu_item_index*y_spacing)))
            destination_surface.blit(text_surface, text_rect)
    
        menu_item_index += 1
    ...

def get_next_menu_item(menu: list, current_selection: str):
    index = 0
    for menu_item in menu:
        if menu_item["name"] == current_selection:
            index += 1
            if index > len(menu) - 1:
                index = 0
            return menu[index]["name"]
        index += 1

def get_previous_menu_item(menu: list, current_selection: str):
    index = 0
    for menu_item in menu:
        if menu_item["name"] == current_selection:
            index -= 1
            if index < 0:
                index = len(menu) - 1
            return menu[index]["name"]
        index += 1
    # return current_selection
