from src.state import State
from src.screens.videocallcutscene.resources import *

class Wait(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.args = args[0]
        self.wait_time = self.args[0]
        self.status = "waiting"
    
    def update(self, video_call_cutscene):
        if self.status == "waiting":
            if video_call_cutscene.game.is_button_released(START_BUTTON):
                self.wait_time = 0
            self.wait_time -= 1

            if self.wait_time < 0:
                self.status = "get_next_event"
                video_call_cutscene.get_next_event()