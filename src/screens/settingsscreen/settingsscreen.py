import logging
import pygame
import math
import os
import json

from settings import *
from src.screens.settingsscreen.screenstates import settings_screen_states
from src.screens.settingsscreen.resources import *
from src.state import State


class SettingsScreen(State):
    def on_state_enter(self, game):

        self.sine_degrees = 0
        self.grow_factor = 0
        self.game = game
        self.background_image = pygame.image.load(self.game.load_resource(BACKGROUND_IMAGE)).convert_alpha()
        '''use this to dim the background image'''
        self.background_image.set_alpha(100)

        self.trees_image = pygame.image.load(self.game.load_resource(TREES_IMAGE)).convert_alpha()
        self.trees_image_wrap = pygame.image.load(self.game.load_resource(TREES_IMAGE)).convert_alpha()
        self.trees_image_position = [0,0]

        self.menu_selection_font = pygame.font.Font(game.load_resource(MENU_SELECTION_FONT),MENU_SELECTION_SIZE)

        self.heading_font = pygame.font.Font(game.load_resource(HEADING_FONT), HEADING_SIZE)
        self.heading_text_surface = None

        game.play_music(SETTINGS_SCREEN_MUSIC)
        
        self.state = State(settings_screen_states)
        self.state.start(self, "fade_in")
    
    def set_heading_text(self, new_text):
        self.heading_text_surface = self.heading_font.render(new_text,True,MAIN_TEXT_COLOR)

    def process_events(self, game):
        if game.game_should_quit():
            game.quit_game()

        self.state.process_events(self)

    def update(self, game):
        self.grow_factor = int(math.sin(self.sine_degrees) * max_text_grow)
        self.sine_degrees += text_grow_step_size%max_text_grow
        self.state.update(self)

    def draw(self, game):
        game.get_screen().fill("#000000")
        game.get_screen().blit(self.background_image, (0,0))
        game.get_screen().blit(self.trees_image, self.trees_image_position)
        if self.heading_text_surface is not None:
            text_rect = self.heading_text_surface.get_rect(center=(SCREEN_WIDTH/2, select_a_file_text_y_position))
            game.get_screen().blit(self.heading_text_surface, text_rect) 
        self.state.draw(self)

    def go_to_title_screen(self):
        self.state.set_state(self, "go_to_title_screen")

    def select_setting(self):
        self.state.set_state(self, "select_setting")

    def display_settings(self):
        self.state.set_state(self, "display_settings")