import pygame
from src.state import State
from src.screens.videocallcutscene.resources import *

class EndCall(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.args = args[0]
        self.next_game_state = self.args[0]
        self._wait_timer = 120
        self.status = "end_call"
    
    # def load_next_game_state(self, video_call_cutscene):
    #     if self.next_game_state == "world_map":
    #         video_call_cutscene.game.load_world_map()
        ...

    def on_state_enter(self, video_call_cutscene):
        self.video_call_blank_background = pygame.image.load(video_call_cutscene.game.load_resource(VIDEO_CALL_BLANK_BACKGROUND_PATH))
        self.video_call_blank_background_rect = self.video_call_blank_background.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
        video_call_cutscene.game.play_sound(VIDEO_CALL_DECLINE_SOUND_PATH)

    def update(self, video_call_cutscene):
        if self.status == "end_call":
            self._wait_timer -= 1
            if self._wait_timer < 0:
                self._wait_timer = 120
                self.status = "load_next_game_state"
        
        elif self.status == "load_next_game_state":
            self._wait_timer -= 1
            if self._wait_timer < 0:
                self._wait_timer = 120
                self.status = "end"
                video_call_cutscene.load_next_game_state(self.next_game_state)
    
    def draw(self, video_call_cutscene):
        if self.status == "end_call":
            video_call_cutscene.game.get_screen().fill("#000000")
            video_call_cutscene.game.get_screen().blit(self.video_call_blank_background,self.video_call_blank_background_rect)

        elif self.status == "load_next_game_state" or "end":
            video_call_cutscene.game.get_screen().fill("#000000")

    ...