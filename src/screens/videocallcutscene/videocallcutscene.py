import pygame
import logging

from settings import *
from src.state import State
from src.screens.videocallcutscene.screenstates import cutscenes

VIDEO_CALL_WINDOW_BORDER_COLOR = "#5b6063"
TEXT_BOX_Y_POSITION = 174
WINDOW_Y_POSITION = 54

class VideoCallCutscene(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.cutscene_name = args[0]
        self.cutscenes = cutscenes
        self.event_index = 0
        self.text_box = {"path": None, "position" : [120,TEXT_BOX_Y_POSITION], "image" : None}
        self.backgrounds = {
                            1 : {"path": None, "position" : [120, WINDOW_Y_POSITION], "image" : None},
                            2 : {"path": None, "position" : [264, WINDOW_Y_POSITION], "image" : None}
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
    
    def go_to_next_event(self, cutscene_name):
        states = self.get_states_from_cutscene(cutscene_name)
        self.state = State(states)
        self.event_index = 0
        self.state.start(self,self.event_index)
    
    def load_next_game_state(self, next_state):

        self.game.save_game()
        
        if next_state == "world_map":
            self.game.load_world_map()
    
    def process_events(self, game):
        if game.game_should_quit():
            game.quit_game()
        self.state.process_events(self)
    
    def update(self, game):
        for character_animation in self.character_animations:
            if self.character_animations[character_animation]["animated_sprite"] is not None:
                self.character_animations[character_animation]["animated_sprite"].update()

        self.state.update(self)
    
    def draw(self, game):
        game.get_screen().fill("#000000")

        background_index = 0
        for background in self.backgrounds:
            # draw zoom call "cameras"
            if self.backgrounds[background]["image"] is not None:
                

                character_animation_index = background_index + 1

                if character_animation_index in self.character_animations:
                    if self.character_animations[character_animation_index]["animated_sprite"] is not None:
                        character_animation = self.character_animations[character_animation_index]["animated_sprite"]
                        character_animation.set_position(self.backgrounds[background]["position"][0], self.backgrounds[background]["position"][1])
                        character_animation.set_position(0,0)
                        character_animation.draw()
                        
                        # print(character_animation.frames)
                        
                game.get_screen().blit(self.backgrounds[background]["image"], self.backgrounds[background]["position"])
                # game.get_screen().blit(character_animation.get_frame_image(), (self.backgrounds[background]["position"][0], self.backgrounds[background]["position"][1]))

                # draw blue rectangle around background to make it look like a zoom call
                video_call_window_rect = self.backgrounds[background]["image"].get_rect()
                video_call_window_rect[0] = self.backgrounds[background]["position"][0]
                video_call_window_rect[1] = self.backgrounds[background]["position"][1]
                pygame.draw.rect(game.get_screen(), VIDEO_CALL_WINDOW_BORDER_COLOR, video_call_window_rect,1, border_radius=2)
            
            background_index += 1
            
            # draw the text box
            if self.text_box["image"] is not None:
                ...
                game.get_screen().blit(self.text_box["image"], self.text_box["position"])


                # video_call_window_rect = self.backgrounds[background]["image"].get_rect()
                # video_call_window_rect[0] = self.backgrounds[background]["position"][0]
                # video_call_window_rect[1] = self.backgrounds[background]["position"][1]
        self.state.draw(self)

    def get_next_event(self):
        self.event_index += 1
        if self.event_index in self.state.states:
            self.state.set_state(self, self.event_index, self.state.states[self.event_index][1])
        else:
            logging.debug(f"could not get next video call cutscene event!")

# cutscene_states = {"ringing": VideoCallRinging}