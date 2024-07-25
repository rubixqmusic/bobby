import pygame
import textwrap
import math

from src.state import State
from src.screens.videocallcutscene.resources import *

class Choice(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)

        MAX_LINES = 2
        TEXT_SIZE = 16
        MAX_LINE_WIDTH = 32
        self.args = args[0]
        self.dialog = self.args[0]
        self.choices_args = self.args[1]
        self.choices = []
        self.choice = ""
        self.x_start = 124
        self.x_spacing = 40
        self.y_start = 196

        self.max_text_grow = 5.0
        self.text_grow_step_size = 0.1
        self.sine_degrees = 0
        self.grow_factor = 0

        
        self.text_surfaces = {}
        self.text_lines = textwrap.wrap(self.dialog, MAX_LINE_WIDTH)
        self.number_of_lines = len(self.text_lines)

        self.text_positions = [
                                [124, 178],
                                [124, 196]
        ]

        self.current_character = 0
        self.current_line = 0

        self.status = "get_next_character"


        for choice in self.choices_args:
            new_choice = {}
            new_choice[choice[0]] = choice[1]
            new_choice["name"] = choice[0]
            new_choice["text"] = choice[0]
            self.choices.append(new_choice)

            # self.choices[]
    
    def on_state_enter(self, video_call_cutscene):
        self.font = pygame.font.Font(video_call_cutscene.game.load_resource(DIALOG_FONT_PATH), DIALOG_SIZE)
    
    def update(self, video_call_cutscene):
        self.grow_factor = int(math.sin(self.sine_degrees) * self.max_text_grow)
        self.sine_degrees += self.text_grow_step_size%self.max_text_grow

        if self.status == "get_next_character":
            if self.current_line > len(self.text_lines) -1:
                self.current_line = 0
                self.choice = self.choices[0]["name"]
                self.status = "make_choice"
            elif self.current_character > len(self.text_lines[self.current_line]):
                self.current_character = 0
                self.current_line += 1   
            else:
                new_text = self.text_lines[self.current_line][0:self.current_character]
                new_text_surface = self.font.render(new_text,True,DIALOG_COLOR)
                self.text_surfaces[self.current_line] = new_text_surface
                self.current_character += 1
                video_call_cutscene.game.play_sound(DIALOG_SOUND_PATH)
        
        elif self.status == "make_choice":
            if video_call_cutscene.game.is_button_released(START_BUTTON) or video_call_cutscene.game.is_button_released(ACTION_BUTTON_1):
                for choice in self.choices:
                    if choice["name"] == self.choice:
                        # video_call_cutscene.game.play_sound(video_call_cutscene.game.load_resource(VIDEO_CALL_ACCEPT_SOUND_PATH))
                        next_event = choice[self.choice]
                        states = video_call_cutscene.get_states_from_cutscene(next_event)
                        video_call_cutscene.state = State(states)
                        video_call_cutscene.event_index = -1
                        video_call_cutscene.get_next_event()
            elif video_call_cutscene.game.is_button_released(RIGHT_BUTTON):
                video_call_cutscene.game.play_sound(VIDEO_CALL_SELECT_SOUND_PATH)
                self.choice = self.get_next_menu_item(self.choices, self.choice)
            elif video_call_cutscene.game.is_button_released(LEFT_BUTTON):
                video_call_cutscene.game.play_sound(VIDEO_CALL_SELECT_SOUND_PATH)
                self.choice = self.get_previous_menu_item(self.choices, self.choice)

    
    def draw(self, video_call_cutscene):
        if self.text_surfaces != {}:
            for text_surface in self.text_surfaces:
                video_call_cutscene.game.get_screen().blit(self.text_surfaces[text_surface], self.text_positions[text_surface])

        if self.status == "get_next_character":
            if video_call_cutscene.backgrounds[1]["image"] is not None:
                    current_speaker_rect = video_call_cutscene.backgrounds[1]["image"].get_rect(topleft=video_call_cutscene.backgrounds[1]["position"])
                    pygame.draw.rect(video_call_cutscene.game.get_screen(), CURRENT_SPEAKER_COLOR, current_speaker_rect, 1, border_radius=2)
        elif self.status == "make_choice":
            self.draw_menu(self.choices,self.choice, self.x_start, self.x_spacing, self.font, DIALOG_COLOR, video_call_cutscene.game.get_screen(), self.grow_factor)
    
    def draw_menu(self,
              menu: list, 
              current_selection: str, 
              x_start: int, 
              x_spacing: int, 
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
                drop_shadow_surface = font.render(menu_item['text'],False,drop_shadow_color)
            
            if menu_item["name"] == current_selection:
                if drop_shadow_surface is not None:
                    drop_shadow_surface_new = pygame.transform.scale(drop_shadow_surface, 
                                        (text_surface_base_size[0] + grow_factor, 
                                        text_surface_base_size[1] + grow_factor))
                    drop_shadow_rect = drop_shadow_surface_new.get_rect(topleft=(drop_shadow_x, x_start + (menu_item_index*x_spacing)+drop_shadow_y, self.y_start))
                    destination_surface.blit(drop_shadow_surface, drop_shadow_rect)
                
                new_surface = pygame.transform.scale(text_surface, 
                                        (text_surface_base_size[0] + grow_factor, 
                                        text_surface_base_size[1] + grow_factor))
                text_rect = new_surface.get_rect(topleft=(x_start + (menu_item_index*x_spacing), self.y_start))
                destination_surface.blit(new_surface, text_rect)
            else:
                if drop_shadow_surface is not None:
                    drop_shadow_rect = drop_shadow_surface.get_rect(center=( x_start + (menu_item_index*x_spacing)+drop_shadow_y,self.y_start+drop_shadow_y))
                    destination_surface.blit(drop_shadow_surface, drop_shadow_rect)
                text_rect = text_surface.get_rect(topleft=(x_start + (menu_item_index*x_spacing), self.y_start))
                destination_surface.blit(text_surface, text_rect)
        
            menu_item_index += 1
    ...

    def get_next_menu_item(self, menu: list, current_selection: str):
        index = 0
        for menu_item in menu:
            if menu_item["name"] == current_selection:
                index += 1
                if index > len(menu) - 1:
                    index = 0
                return menu[index]["name"]
            index += 1

    def get_previous_menu_item(self, menu: list, current_selection: str):
        index = 0
        for menu_item in menu:
            if menu_item["name"] == current_selection:
                index -= 1
                if index < 0:
                    index = len(menu) - 1
                return menu[index]["name"]
            index += 1
        # return current_selection