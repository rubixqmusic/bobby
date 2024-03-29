import logging
import pygame

from res.framework.state import State
from res.settings import *

class Init(State):
    def on_state_enter(self, game):
        logging.debug(f"loaded init state")
        if DEBUG_ENABLED:
            if DEBUG_START_IN_STATE == "title_screen":
                game.load_title_screen()
            elif DEBUG_START_IN_STATE == "file_select_screen":
                game.load_file_select_screen()
            elif DEBUG_START_IN_STATE == "video_call_cutscene":
                game.run_video_call_cutscene(DEBUG_VIDEO_CALL_CUTSCENE)
            elif DEBUG_START_IN_STATE == "world_map":
                game.load_world_map()

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