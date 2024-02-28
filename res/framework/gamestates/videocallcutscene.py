import pygame
import logging

from res.settings import *
from res.framework.state import State
from res.framework.gamestates.videocallcutscenestates import VideoCallRinging



class VideoCallCutscene(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.cutscene_name = args[0]
        self.sequence_index = 0
        
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
    
    def draw(self, object):
        self.state.draw(self)

cutscene_states = {"ringing": VideoCallRinging}