import pygame
import logging

from res.settings import *
from res.framework.state import State
from res.framework.gamestates.videocallcutscenestates import VideoCallRinging


class VideoCallCutscene(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.cutscene_name = args[0]
        self.event_index = 0
        
    def on_state_enter(self, game):
        self.game = game
        self.state = State(cutscene_states)
        self.state.start(self,"ringing")
    
    def process_events(self, game):
        if game.game_should_quit():
            game.quit_game()
        self.state.process_events(self)
    
    def update(self, game):
        self.state.update(self)
    
    def draw(self, game):
        self.state.draw(self)

    def get_next_event(self):
        self.event_index += 1
        if self.event_index in self.states:
            self.state.set_state(self, self.event_index, self.states[self.event_index][1])
        else:
            logging.debug(f"could not get next video call cutscene event!")

cutscene_states = {"ringing": VideoCallRinging}