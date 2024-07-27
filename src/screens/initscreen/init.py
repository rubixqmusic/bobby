import logging
import pygame

from src.state import State
from src.screens.initscreen.screenstates import *
from settings import *

class Init(State):
    def on_state_enter(self, game):

        self.state = State(init_screen_states)
        self.game = game

        logging.debug(f"game has been initialized")
        if DEBUG_ENABLED:
            if DEBUG_START_IN_STATE == "title_screen":
                game.load_title_screen()
            elif DEBUG_START_IN_STATE == "file_select_screen":
                game.load_file_select_screen()
            elif DEBUG_START_IN_STATE == "settings_screen":
                game.load_settings_screen()
            elif DEBUG_START_IN_STATE == "video_call_cutscene":
                game.run_video_call_cutscene(DEBUG_VIDEO_CALL_CUTSCENE)
            elif DEBUG_START_IN_STATE == "world_map":
                game.load_world_map()
            elif DEBUG_START_IN_STATE == "gameplay":
                game.load_level(DEBUG_LEVEL_NAME, DEBUG_LEVEL_START_POSITION, DEBUG_LEVEL_START_TRANSITION)
            elif DEBUG_START_IN_STATE == "splashscreen":
                game.load_splashscreen()
            elif DEBUG_START_IN_STATE == "init_screen":
                self.control_notification()

            else:
                logging.debug(f"no DEBUG_START_IN_STATE named {DEBUG_START_IN_STATE}, loading title screen instead")
                self.control_notification()
            
        else:
            self.control_notification()
    
    def load_splashscreen(self):
        self.game.load_splashscreen()

    def control_notification(self):
        self.state.set_state(self, "control_notification")

    def process_events(self, game):
        self.state.process_events(self)
    
    def draw(self, game):
        self.state.draw(self)

    def update(self, game):
        self.state.update(self)
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         game.quit_game()

        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_ESCAPE:
        #             game.quit_game()