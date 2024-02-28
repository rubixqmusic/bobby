import pygame
import logging

from res.settings import *
from res.framework.state import State

VIDEO_CALL_RINGING_IMAGE_PATH = f"{GRAPHICS_PATH}/video_call_cutscenes/video_call_ringing.png"

class VideoCallRinging(State):
    ...
    def on_state_enter(self, video_call_cutscene):
        self.selection = "accept"
        self.status = "ringing"
        self.video_call_ringing_image = pygame.image.load(video_call_cutscene.game.load_resource(VIDEO_CALL_RINGING_IMAGE_PATH))
        self.video_call_ringing_rect = self.video_call_ringing_image.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))

        video_call_cutscene.game.stop_music()

        # stop all music and play ringing sound
        ...
    
    def update(self, video_call_cutscene):
        if self.status == "ringing":
            if video_call_cutscene.game.is_button_released("left_button"):
                if self.selection == "accept":
                    self.selection = "decline"
                elif self.selection == "delcine":
                    self.selection = "accept"
            if video_call_cutscene.game.is_button_released("right_button"):
                if self.selection == "accept":
                    self.selection = "decline"
                elif self.selection == "delcine":
                    self.selection = "accept"
            
            if video_call_cutscene.game.is_button_released("start_button"):
                if self.selection == "delcine":
                    self.status = "delcine"
                if self.selection == "accept":
                    self.status = "accept"

        elif self.status == "delcine":
            ...
        
        elif self.status == "accept":
            ...
    
    def draw(self, video_call_cutscene):
        if self.status == "ringing":
            video_call_cutscene.game.get_screen().fill("#000000")
            video_call_cutscene.game.get_screen().blit(self.video_call_ringing_image,self.video_call_ringing_rect)
            