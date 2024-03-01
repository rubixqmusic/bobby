import pygame
import logging

from res.settings import *
from res.framework.state import State
from res.framework.gamestates.videocallcutscenestates import VideoCallRinging
from res.framework.videocallcutscenes import cutscenes


class VideoCallCutscene(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.cutscene_name = args[0]
        self.cutscenes = cutscenes
        self.event_index = 0
        self.backgrounds = {
                            1 : {"path": None, "position" : [125, 70], "image" : None},
                            2 : {"path": None, "position" : [275, 70], "image" : None}
                            }
        self.character_animations = {
                                    1 : {"spritesheet_path": None, "animation_path" : None, "starting_animation" : None, "animated_sprite" : None},
                                    2 : {"spritesheet_path": None, "animation_path" : None, "starting_animation" : None, "animated_sprite" : None}
                                    }
        
    def get_states_from_cutscene(self, cutscene_name):
        if cutscene_name in self.cutscenes:
            new_states = {}
            index = 0
            for cutscene_event in self.cutscenes[cutscene_name]:
                new_states[index] = cutscene_event[0], cutscene_event[1]
                index += 1
            return new_states
        
    def on_state_enter(self, game):
        self.game = game
        states = self.get_states_from_cutscene(self.cutscene_name)
        self.state = State(states)
        self.event_index = 0
        self.state.start(self,self.event_index)
    
    def process_events(self, game):
        if game.game_should_quit():
            game.quit_game()
        self.state.process_events(self)
    
    def update(self, game):
        self.state.update(self)
    
    def draw(self, game):
        game.get_screen().fill("#000000")
        for background in self.backgrounds:
            if self.backgrounds[background]["image"] is not None:
                game.get_screen().blit(self.backgrounds[background]["image"], self.backgrounds[background]["position"])
        self.state.draw(self)

    def get_next_event(self):
        self.event_index += 1
        if self.event_index in self.state.states:
            self.state.set_state(self, self.event_index, self.state.states[self.event_index][1])
        else:
            logging.debug(f"could not get next video call cutscene event!")

cutscene_states = {"ringing": VideoCallRinging}