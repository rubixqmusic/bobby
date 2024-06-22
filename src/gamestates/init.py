import logging
import pygame

from src.state import State
from settings import *

class Init(State):
    def on_state_enter(self, game):
        logging.debug(f"game has been initialized")
        if DEBUG_ENABLED:
            if DEBUG_START_IN_STATE == "title_screen":
                game.load_title_screen()
            elif DEBUG_START_IN_STATE == "file_select_screen":
                game.load_file_select_screen()
            elif DEBUG_START_IN_STATE == "video_call_cutscene":
                game.run_video_call_cutscene(DEBUG_VIDEO_CALL_CUTSCENE)
            elif DEBUG_START_IN_STATE == "world_map":
                game.load_world_map()
            elif DEBUG_START_IN_STATE == "playing_level":
                game.load_level(DEBUG_LEVEL_NAME, DEBUG_LEVEL_START_POSITION, DEBUG_LEVEL_START_TRANSITION)
            elif DEBUG_START_IN_STATE == "splashscreen":
                game.load_splashscreen()

            else:
                logging.debug(f"no DEBUG_START_IN_STATE named {DEBUG_START_IN_STATE}, loading title screen instead")
                game.load_title_screen()
            
        else:
            game.load_splashscreen()


    def process_events(self, game):
        ...
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         game.quit_game()

        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_ESCAPE:
        #             game.quit_game()