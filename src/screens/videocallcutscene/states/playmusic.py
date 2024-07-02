from src.state import State
from src.screens.videocallcutscene.resources import *

class PlayMusic(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.args = args[0]
        self.song_name = self.args[0]
        self.volume = self.args[1]

    def on_state_enter(self, video_call_cutscene):
        video_call_cutscene.game.play_music(f"{MUSIC_PATH}/{self.song_name}", self.volume)
        video_call_cutscene.get_next_event()