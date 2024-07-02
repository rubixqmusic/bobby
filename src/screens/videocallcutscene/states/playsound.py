from src.state import State
from src.screens.videocallcutscene.resources import *

class PlaySound(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.args = args[0]
        self.sound_name = self.args[0]

    def on_state_enter(self, video_call_cutscene):
        video_call_cutscene.game.play_sound(f"{SOUNDS_PATH}/{self.sound_name}")
        video_call_cutscene.get_next_event()