import logging
import pygame
import math

from res.settings import *
from res.framework.state import State

background_image_path = f"{GRAPHICS_PATH}/backgrounds/title_screen_background.png"
trees_image_path = f"{GRAPHICS_PATH}/backgrounds/title_screen_trees.png"
title_screen_music_path = f"{MUSIC_PATH}/title_screen.mp3"
title_screen_text_path = f"{GRAPHICS_PATH}/backgrounds/title_screen_text.png"
title_screen_menu_select_sound_path = f"{SOUNDS_PATH}/menu_select.wav"
title_screen_menu_select_sound_volume = 0.7
coin_sound_path = f"{SOUNDS_PATH}/coin.wav"

LETS_GO_FX = f"{SOUNDS_PATH}/lets_go.wav"
FUCK_YOU_FX = f"{SOUNDS_PATH}/fuck_you.wav"
STORY_MODE_FX = f"{SOUNDS_PATH}/story_mode.wav"
BACK_FX = f"{SOUNDS_PATH}/video_call_decline.wav"

BACKGROUND_ALPHA = 256

BACKGROUND_SCROLL_SPEED = 50

scroll_speed = 1

menu_selection_font_path = f"{FONTS_PATH}/{DEFAULT_FONT}"
menu_selection_text_size = 16
licensed_by_kablio_text_size = 12
main_text_color = f"#fbcb1d"
menu_selection_text_color = f"#fe112b"
menu_drop_shadow_x = 1
menu_drop_shadow_y = 1
menu_drop_shadow_color = f"#000000"

licensed_by_kablio_text = f"Licensed By Kablio©"
licensed_by_kablio_text_y_position = 272

text_y_spacing = 25
max_text_grow = 5.0
text_grow_step_size = 0.1
sine_degrees = 0.0
grow_factor = 0


class TitleScreen(State):
    def on_state_enter(self, game):

        game.set_current_save_file("")
        
        self.sine_degrees = 0
        self.grow_factor = 0
        self.game = game

        self.background_scroll_step = 0

        self.background_image = pygame.image.load(self.game.load_resource(background_image_path)).convert_alpha()
        self.background_image.set_alpha(BACKGROUND_ALPHA)
        self.background_image_wrap = pygame.image.load(self.game.load_resource(background_image_path)).convert_alpha()
        self.background_image_wrap.set_alpha(BACKGROUND_ALPHA)

        self.trees_image = pygame.image.load(self.game.load_resource(trees_image_path)).convert_alpha()
        self.trees_image_wrap = pygame.image.load(self.game.load_resource(trees_image_path)).convert_alpha()

        self.menu_selection_font = pygame.font.Font(game.load_resource(menu_selection_font_path),menu_selection_text_size)
        self.licensed_by_kablio_font = pygame.font.Font(game.load_resource(menu_selection_font_path), licensed_by_kablio_text_size)

        self.background_image_position = [0,0]
        self.background_image_wrap_position = [self.background_image_position[0] + self.background_image.get_width(), self.background_image_position[1]]
        
        self.trees_image_position = [0,0]
        self.trees_image_wrap_position = [self.trees_image_position[0] + self.trees_image.get_width(), self.trees_image_position[1]]

        self.title_text_image = pygame.image.load(self.game.load_resource(title_screen_text_path)).convert_alpha()
        self.licensed_by_kablio_text_surface = self.licensed_by_kablio_font.render(licensed_by_kablio_text,True,main_text_color)

        game.play_music(game.load_resource(title_screen_music_path))
        
        self.state = State(title_screen_states)
        self.state.start(self, "fade_in")

    def process_events(self, game):
        self.state.process_events(self)

    def update(self, game):
        self.grow_factor = int(math.sin(self.sine_degrees) * max_text_grow)
        self.sine_degrees += text_grow_step_size%max_text_grow

        self.background_scroll_step += 1
        self.background_scroll_step = self.background_scroll_step%BACKGROUND_SCROLL_SPEED

        if self.background_scroll_step == 0:
            self.background_image_position[0] -= 1

        if self.background_image_position[0] + self.background_image.get_width() < 0:
            self.background_image_position[0] += self.background_image.get_width()
        self.background_image_wrap_position[0] = self.background_image_position[0] + self.background_image.get_width()

        self.trees_image_position[0] -= scroll_speed
        if self.trees_image_position[0] + self.trees_image.get_width() < 0:
            self.trees_image_position[0] += self.trees_image.get_width()

        self.trees_image_wrap_position[0] = self.trees_image_position[0] + self.trees_image.get_width()

        self.state.update(self)

    def draw(self, game):
        text_rect = self.licensed_by_kablio_text_surface.get_rect(center=(SCREEN_WIDTH/2, licensed_by_kablio_text_y_position))
        game.get_screen().fill("#000000")
        game.get_screen().blit(self.background_image, self.background_image_position)
        game.get_screen().blit(self.background_image_wrap, self.background_image_wrap_position)
        game.get_screen().blit(self.trees_image, self.trees_image_position)
        game.get_screen().blit(self.trees_image_wrap, self.trees_image_wrap_position)
        game.get_screen().blit(self.title_text_image, (0,0))
        game.get_screen().blit(self.licensed_by_kablio_text_surface, text_rect)
        self.state.draw(self)


class FadeIn(State):
    def on_state_enter(self, title_screen):
        self.min_fade = 0
        self.max_fade = 255
        self.fade = self.min_fade
        self.fade_step = 5
    
    def draw(self, title_screen):
        if self.fade < self.max_fade:
            title_screen.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
            self.fade += self.fade_step
        else:
            title_screen.state.set_state(title_screen, "start_game_or_quit")


class FadeOutAndQuit(State):
    def on_state_enter(self, title_screen):
        self.min_fade = 0
        self.max_fade = 255
        self.fade = self.max_fade
        self.fade_step = 5
    
    def draw(self, title_screen):
        if self.fade > self.min_fade:
            title_screen.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
            self.fade -= self.fade_step
        else:
            self.fade = 0
            title_screen.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
            title_screen.game.quit_game()


class GoToFileSelectScreen(State):
    def on_state_enter(self, title_screen):
        self.min_fade = 0
        self.max_fade = 255
        self.fade = self.max_fade
        self.fade_step = 5
    
    def draw(self, title_screen):
        if self.fade > self.min_fade:
            title_screen.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
            self.fade -= self.fade_step
        else:
            self.fade = 0
            title_screen.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
            title_screen.game.load_file_select_screen()
            # title_screen.game.quit_game()    


class StartGameOrQuit(State):
    def on_state_enter(self, title_screen): 
        self.text_y_start_position = 170        
        self.current_menu_selection = "start_game"

        self.menu = [
                        {"name" : "start_game", "text" : "Start Game"},
                        # {"name" : "settings", "text" : "Settings"},
                        {"name" : "quit_game", "text" : "Quit Game"}
                    ]
    
    def process_events(self, title_screen):            
        if title_screen.game.is_button_released(DOWN_BUTTON):
                self.current_menu_selection = get_next_menu_item(self.menu, self.current_menu_selection)
                title_screen.game.play_sound(title_screen.game.load_resource(title_screen_menu_select_sound_path))

        if title_screen.game.is_button_released(UP_BUTTON):
            self.current_menu_selection = get_previous_menu_item(self.menu, self.current_menu_selection)
            title_screen.game.play_sound(title_screen.game.load_resource(title_screen_menu_select_sound_path))

        if title_screen.game.is_button_released(START_BUTTON):
            if self.current_menu_selection == "start_game":
                title_screen.game.play_sound(title_screen.game.load_resource(LETS_GO_FX))
                title_screen.state.set_state(title_screen, "pick_game_mode")

            if self.current_menu_selection == "quit_game":
                title_screen.game.play_sound(title_screen.game.load_resource(FUCK_YOU_FX))
                title_screen.game.stop_music()
                title_screen.state.set_state(title_screen, "fade_out_and_quit")

    def draw(self, title_screen):
        draw_menu(self.menu, 
                  self.current_menu_selection, 
                  self.text_y_start_position, 
                  text_y_spacing, 
                  title_screen.menu_selection_font, 
                  menu_selection_text_color,
                  title_screen.game.get_screen(),
                  title_screen.grow_factor,
                  True)


class PickGameMode(State):
    def on_state_enter(self, title_screen):
        self.text_y_start_position = 170        
        self.current_menu_selection = "story_mode"

        self.menu = [
                        {"name" : "story_mode", "text" : "Story Mode"},
                        {"name" : "2_player", "text" : "2 Player"},
                        {"name" : "back", "text" : "Back"}
                    ]
    
    def process_events(self, title_screen):
            if title_screen.game.is_button_released(DOWN_BUTTON):
                self.current_menu_selection = get_next_menu_item(self.menu, self.current_menu_selection)
                title_screen.game.play_sound(title_screen.game.load_resource(title_screen_menu_select_sound_path))

            if title_screen.game.is_button_released(UP_BUTTON):
                self.current_menu_selection = get_previous_menu_item(self.menu, self.current_menu_selection)
                title_screen.game.play_sound(title_screen.game.load_resource(title_screen_menu_select_sound_path))

            if title_screen.game.is_button_released(START_BUTTON):
                if self.current_menu_selection == "back":
                    title_screen.game.play_sound(title_screen.game.load_resource(BACK_FX))
                    title_screen.state.set_state(title_screen, "start_game_or_quit")
            
            if title_screen.game.is_button_released(START_BUTTON):
                if self.current_menu_selection == "story_mode":
                    title_screen.game.play_sound(title_screen.game.load_resource(STORY_MODE_FX))
                    title_screen.state.set_state(title_screen, "go_to_file_select_screen")
    
    def draw(self, title_screen):
        draw_menu(self.menu, 
                  self.current_menu_selection, 
                  self.text_y_start_position, 
                  text_y_spacing, 
                  title_screen.menu_selection_font, 
                  menu_selection_text_color,
                  title_screen.game.get_screen(),
                  title_screen.grow_factor,
                  True)

title_screen_states = {
                        "fade_in" : FadeIn,
                        "start_game_or_quit" : StartGameOrQuit,
                        "pick_game_mode" : PickGameMode,
                        "go_to_file_select_screen" : GoToFileSelectScreen,
                        "fade_out_and_quit" : FadeOutAndQuit
                        }

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
