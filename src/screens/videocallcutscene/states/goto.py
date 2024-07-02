from src.state import State
from src.screens.videocallcutscene.resources import *

class GoTo(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.args = args[0]
        self.next_cutscene = self.args[0]

    def on_state_enter(self, video_call_cutscene):
        states = video_call_cutscene.get_states_from_cutscene(self.next_cutscene)
        video_call_cutscene.state = State(states)
        video_call_cutscene.event_index = -1
        video_call_cutscene.get_next_event()