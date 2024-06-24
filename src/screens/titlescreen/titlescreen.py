import logging
import pygame
import math

from settings import *
from src.screens.titlescreen.resources import *
from src.screens.titlescreen.screenstates import title_screen_states
from src.state import State


class TitleScreen(State):
    def on_state_enter(self, game):

        logging.debug(f"title screen loaded")
        game.set_current_save_file("")
        
        self.sine_degrees = 0
        self.grow_factor = 0
        self.game = game

        self.background_scroll_step = 0

        self.background_image = pygame.image.load(self.game.load_resource(background_image_path)).convert_alpha()
        self.background_image.set_alpha(BACKGROUND_ALPHA)
        self.background_image_wrap = pygame.image.load(self.game.load_resource(background_image_path)).convert_alpha()
        self.background_image_wrap.set_alpha(BACKGROUND_ALPHA)

        self.trees_image = pygame.image.load(self.game.load_resource(trees_image_path)).convert_alpha()
        self.trees_image_wrap = pygame.image.load(self.game.load_resource(trees_image_path)).convert_alpha()

        self.menu_selection_font = pygame.font.Font(game.load_resource(menu_selection_font_path),menu_selection_text_size)
        self.licensed_by_kablio_font = pygame.font.Font(game.load_resource(menu_selection_font_path), licensed_by_kablio_text_size)

        self.background_image_position = [0,0]
        self.background_image_wrap_position = [self.background_image_position[0] + self.background_image.get_width(), self.background_image_position[1]]
        
        self.trees_image_position = [0,0]
        self.trees_image_wrap_position = [self.trees_image_position[0] + self.trees_image.get_width(), self.trees_image_position[1]]

        self.title_text_image = pygame.image.load(self.game.load_resource(title_screen_text_path)).convert_alpha()
        self.licensed_by_kablio_text_surface = self.licensed_by_kablio_font.render(licensed_by_kablio_text,True,main_text_color)

        game.play_music(title_screen_music_path)
        
        self.state = State(title_screen_states)
        self.state.start(self, "fade_in")

    def process_events(self, game):
        self.state.process_events(self)

    def update(self, game):
        self.grow_factor = int(math.sin(self.sine_degrees) * max_text_grow)
        self.sine_degrees += text_grow_step_size%max_text_grow

        self.background_scroll_step += 1
        self.background_scroll_step = self.background_scroll_step%BACKGROUND_SCROLL_SPEED

        if self.background_scroll_step == 0:
            self.background_image_position[0] -= 1

        if self.background_image_position[0] + self.background_image.get_width() < 0:
            self.background_image_position[0] += self.background_image.get_width()
        self.background_image_wrap_position[0] = self.background_image_position[0] + self.background_image.get_width()

        self.trees_image_position[0] -= scroll_speed
        if self.trees_image_position[0] + self.trees_image.get_width() < 0:
            self.trees_image_position[0] += self.trees_image.get_width()

        self.trees_image_wrap_position[0] = self.trees_image_position[0] + self.trees_image.get_width()

        self.state.update(self)

    def draw(self, game):
        text_rect = self.licensed_by_kablio_text_surface.get_rect(center=(SCREEN_WIDTH/2, licensed_by_kablio_text_y_position))
        game.get_screen().fill("#000000")
        game.get_screen().blit(self.background_image, self.background_image_position)
        game.get_screen().blit(self.background_image_wrap, self.background_image_wrap_position)
        game.get_screen().blit(self.trees_image, self.trees_image_position)
        game.get_screen().blit(self.trees_image_wrap, self.trees_image_wrap_position)
        game.get_screen().blit(self.title_text_image, (0,0))
        game.get_screen().blit(self.licensed_by_kablio_text_surface, text_rect)
        self.state.draw(self)

    def go_to_file_select_screen(self):
        self.state.set_state(self, "go_to_file_select_screen")

    def start_game_or_quit(self):
        self.state.set_state(self, "start_game_or_quit")

    def go_to_settings_screen(self):
        self.state.set_state(self, "go_to_settings_screen")

    def fade_out_and_quit(self):
        self.state.set_state(self, "fade_out_and_quit")

