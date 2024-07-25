import pygame
import logging

from src.state import State
from src.screens.videocallcutscene.resources import *

class SetBackgroundImage(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.args = args[0]

        self.background_number = self.args[0]
        self.image_path = self.args[1]
        print(self.background_number)
        print(self.image_path)


    def on_state_enter(self, video_call_cutscene):
        image_path = f"{GRAPHICS_PATH}/{self.image_path}"
        if video_call_cutscene.game.resource_exists(image_path) and self.background_number in video_call_cutscene.backgrounds:
            video_call_cutscene.backgrounds[self.background_number]["path"] = self.image_path
            video_call_cutscene.backgrounds[self.background_number]["image"] = pygame.image.load(video_call_cutscene.game.load_resource(image_path))
        else:
            logging.debug(f"image path is fucked up, homie, this is what you passed in: {image_path}. The fuck am I supposed to do with this??")
        video_call_cutscene.get_next_event()
