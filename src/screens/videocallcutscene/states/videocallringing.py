import pygame
from src.state import State
from src.screens.videocallcutscene.resources import *

class VideoCallRinging(State):
    def on_state_enter(self, video_call_cutscene):
        self.selection = "accept"
        self.status = "decline"
        self.WAIT_TIMER = 120
        
        self.video_call_ringing_image = pygame.image.load(video_call_cutscene.game.load_resource(VIDEO_CALL_RINGING_IMAGE_PATH))
        self.video_call_ringing_rect = self.video_call_ringing_image.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))

        self.video_call_blank_background = pygame.image.load(video_call_cutscene.game.load_resource(VIDEO_CALL_BLANK_BACKGROUND_PATH))
        self.video_call_blank_background_rect = self.video_call_blank_background.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
        self._wait_timer = self.WAIT_TIMER

        self.SELECTION_X = self.video_call_ringing_rect.x
        self.SELECTION_y = self.video_call_ringing_rect.y + 32
        self.SELECTION_RECT_WIDTH = 64
        self.SELECTION_RECT_HEIGHT = 32
        self.SELECTION_RECT_COLOR = "#ffffff"
        self.ACCEPT_X = self.video_call_ringing_rect.x
        self.DECLINE_X = self.video_call_ringing_rect.x + 64

        video_call_cutscene.game.stop_music()
    
    def update(self, video_call_cutscene):
        if self.status == "ringing":
            if video_call_cutscene.game.is_button_released(LEFT_BUTTON):
                video_call_cutscene.game.play_sound(VIDEO_CALL_SELECT_SOUND_PATH)
                if self.selection == "accept":
                    self.selection = "decline"
                elif self.selection == "decline":
                    self.selection = "accept"
            if video_call_cutscene.game.is_button_released(RIGHT_BUTTON):
                video_call_cutscene.game.play_sound(VIDEO_CALL_SELECT_SOUND_PATH)
                if self.selection == "accept":
                    self.selection = "decline"
                elif self.selection == "decline":
                    self.selection = "accept"
            
            if video_call_cutscene.game.is_button_released(START_BUTTON):
                if self.selection == "decline":
                    self.status = "decline"
                    video_call_cutscene.game.stop_music()
                    video_call_cutscene.game.play_sound(VIDEO_CALL_DECLINE_SOUND_PATH)

                if self.selection == "accept":
                    self.status = "accept"
                    video_call_cutscene.game.stop_music()
                    video_call_cutscene.game.play_sound(VIDEO_CALL_ACCEPT_SOUND_PATH)

        elif self.status == "decline":
            self._wait_timer -= 1
            if self._wait_timer < 0:
                self._wait_timer = self.WAIT_TIMER
                self.status = "ringing"
                self.selection = "accept"
                video_call_cutscene.game.play_music(VIDEO_CALL_RINGING_MUSIC_PATH)
        
        elif self.status == "accept":
            self._wait_timer -= 1
            if self._wait_timer < 0:
                self._wait_timer = self.WAIT_TIMER
                self.accept_call_and_get_next_event(video_call_cutscene)
                self.status = "end"
                # self.selection = "accept"
                # video_call_cutscene.game.play_music(video_call_cutscene.game.load_resource(VIDEO_CALL_RINGING_MUSIC_PATH))
            ...
    def accept_call_and_get_next_event(self, video_call_cutscene):
        image_path = VIDEO_CALL_TEXT_BOX_PATH
        if video_call_cutscene.game.resource_exists(image_path):

            # set the cutscene text box image to something other than None so that it is present for each new event in the cutscene
            # until explicitly set to none again
            video_call_cutscene.text_box["path"] = image_path
            video_call_cutscene.text_box["image"] = pygame.image.load(video_call_cutscene.game.load_resource(image_path))
        video_call_cutscene.get_next_event()
        
    def draw(self, video_call_cutscene):
        if self.status == "ringing":
            ringing_image = self.video_call_ringing_image
            
            if self.selection == "accept":
                selection_rect = pygame.rect.Rect(self.ACCEPT_X, self.SELECTION_y, self.SELECTION_RECT_WIDTH, self.SELECTION_RECT_HEIGHT)
            elif self.selection == "decline":
                selection_rect = pygame.rect.Rect(self.DECLINE_X, self.SELECTION_y, self.SELECTION_RECT_WIDTH, self.SELECTION_RECT_HEIGHT)

            video_call_cutscene.game.get_screen().fill("#000000")
            video_call_cutscene.game.get_screen().blit(ringing_image,self.video_call_ringing_rect)
            pygame.draw.rect(video_call_cutscene.game.get_screen(),self.SELECTION_RECT_COLOR,selection_rect,width=2)
            # print(selection_rect)
            # print(self.selection)

        if self.status == "decline":
            video_call_cutscene.game.get_screen().fill("#000000")

        if self.status == "accept":

            video_call_cutscene.game.get_screen().fill("#000000")
            video_call_cutscene.game.get_screen().blit(self.video_call_blank_background,self.video_call_blank_background_rect)