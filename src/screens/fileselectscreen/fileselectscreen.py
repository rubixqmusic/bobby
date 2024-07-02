import logging
import pygame
import math
import os
import json

from src.screens.fileselectscreen.resources import *
from src.screens.fileselectscreen.screenstates import file_select_screen_states
from src.state import State


class FileSelectScreen(State):
    def on_state_enter(self, game):

        self.sine_degrees = 0
        self.grow_factor = 0
        self.game = game
        self.background_image = pygame.image.load(self.game.load_resource(background_image_path)).convert_alpha()
        '''use this to dim the background image'''
        self.background_image.set_alpha(100)

        self.trees_image = pygame.image.load(self.game.load_resource(trees_image_path)).convert_alpha()
        self.trees_image_wrap = pygame.image.load(self.game.load_resource(trees_image_path)).convert_alpha()
        self.trees_image_position = [0,0]

        self.menu_selection_font = pygame.font.Font(game.load_resource(menu_selection_font_path),menu_selection_text_size)

        self.select_a_file_font = pygame.font.Font(game.load_resource(menu_selection_font_path), select_a_file_font_size)
        self.select_a_file_text_surface = None

        self.source_file = ""
        self.destination_file = ""

        game.play_music(file_select_screen_music_path)
        
        
        self.state = State(file_select_screen_states)
        self.state.start(self, "fade_in")
        
    
    def set_select_a_file_text(self, new_text):
        self.select_a_file_text_surface = self.select_a_file_font.render(new_text,True,main_text_color)

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
        if self.select_a_file_text_surface is not None:
            text_rect = self.select_a_file_text_surface.get_rect(center=(SCREEN_WIDTH/2, select_a_file_text_y_position))
            game.get_screen().blit(self.select_a_file_text_surface, text_rect) 
        self.state.draw(self)

    def start_new_game(self):
        self.state.set_state(self, "start_new_game")

    def load_saved_game(self):
        self.state.set_state(self, "load_saved_game")

    def erase_file(self):
        self.state.set_state(self, "erase_file")

    def confirm_erase(self):
        self.state.set_state(self, "confirm_erase")
    
    def file_erased(self):
        self.state.set_state(self, "file_erased")
    
    def select_file(self):
        self.state.set_state(self, "select_file")
    
    def select_source_file(self):
        self.state.set_state(self, "select_source_file")
    
    def select_destination_file(self):
        self.state.set_state(self, "select_destination_file")

    def confirm_copy(self):
        self.state.set_state(self, "confirm_copy")
    
    def file_copied(self):
        self.state.set_state(self, "file_copied")
        

