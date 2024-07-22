import pygame
import textwrap

from src.state import State
from src.screens.videocallcutscene.resources import *

class ShowDialog(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)

        MAX_LINES = 2
        TEXT_SIZE = 16
        MAX_LINE_WIDTH = 32
        # print(self)
        self.args = args[0]
        self.dialog = self.args[0]

        self.sound_speed = 5
        self.sound_speed_step = 0

        self.text_advance_icon_blink_speed = 10
        self.text_advance_icon_step = 0
        self.text_advance_icon_position = [370, 195]
        self.toggle_text_advance_icon = True
        
        
        
        
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
    
    def on_state_enter(self, video_call_cutscene):
        self.current_speaker_font = pygame.font.Font(video_call_cutscene.game.load_resource(DIALOG_FONT_PATH), 10)
        self.text_advance_icon_surface = pygame.image.load(video_call_cutscene.game.load_resource(TEXT_BOX_ADVANCE_ICON))
        self.font = pygame.font.Font(video_call_cutscene.game.load_resource(DIALOG_FONT_PATH), DIALOG_SIZE)
    
    def update(self, video_call_cutscene):

        if self.status == "get_next_character":
            self.sound_speed_step += 1
            self.sound_speed_step = self.sound_speed_step%self.sound_speed
            
    
            if self.current_line > len(self.text_lines) -1:
                self.current_line = 0
                self.status = "wait_for_button"
            elif self.current_character > len(self.text_lines[self.current_line]):
                self.current_character = 0
                self.current_line += 1   
            else:
                new_text = self.text_lines[self.current_line][0:self.current_character]
                new_text_surface = self.font.render(new_text,True,DIALOG_COLOR)
                self.text_surfaces[self.current_line] = new_text_surface
                self.current_character += 1
                if self.sound_speed_step == 0:
                    video_call_cutscene.game.play_sound(DIALOG_SOUND_PATH)
        
        elif self.status == "wait_for_button":
            self.text_advance_icon_step += 1
            self.text_advance_icon_step = self.text_advance_icon_step%self.text_advance_icon_blink_speed
            if self.text_advance_icon_step == 0:
                self.toggle_text_advance_icon = not self.toggle_text_advance_icon

            if video_call_cutscene.game.is_button_released(START_BUTTON) or video_call_cutscene.game.is_button_released(ACTION_BUTTON_1):
                video_call_cutscene.game.play_sound(DIALOG_ADVANCE_SOUND)
                self.status = "get_next_event"
                video_call_cutscene.get_next_event()
    
    def draw(self, video_call_cutscene):
        if self.text_surfaces != {}:
            for text_surface in self.text_surfaces:
                video_call_cutscene.game.get_screen().blit(self.text_surfaces[text_surface], self.text_positions[text_surface])

        if self.status == "get_next_character":
            if video_call_cutscene.backgrounds[1]["image"] is not None:
                current_speaker_rect = video_call_cutscene.backgrounds[1]["image"].get_rect(topleft=video_call_cutscene.backgrounds[1]["position"])
                pygame.draw.rect(video_call_cutscene.game.get_screen(), CURRENT_SPEAKER_COLOR, current_speaker_rect, 5)
                current_speaker_text_surface = self.current_speaker_font.render(f"Cody Feiko", True, "#ffffff", "#000055")
                video_call_cutscene.game.get_screen().blit(current_speaker_text_surface, (video_call_cutscene.backgrounds[1]["position"][0] + 10, video_call_cutscene.backgrounds[1]["position"][1] + 76))
        elif self.status == "wait_for_button":
            if self.toggle_text_advance_icon:
                video_call_cutscene.game.get_screen().blit(self.text_advance_icon_surface, self.text_advance_icon_position)