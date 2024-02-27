import logging
import pygame

from res.framework.state import State
from res.settings import *

class Init(State):
    def on_state_enter(self, game):
        logging.debug(f"loaded init state")
        if DEBUG_ENABLED:
            game.state.set_state(game, DEBUG_START_IN_STATE)
        else:
            game.state.set_state(game, "splashscreen")

    def process_events(self, game):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.quit_game()