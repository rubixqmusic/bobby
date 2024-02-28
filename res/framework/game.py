import pygame
import os
import sys
import logging

from res.settings import *
from res.utilities.ldtk_loader import load_ldtk
from res.framework.state import State
from res.framework.gamestates import init, splashscreen, titlescreen
from res.input_events import *

OFF = 0
PRESSED = 1
RELEASED = 2

class Game:
    def __init__(self) -> None:
        if DEBUG_ENABLED == True:
            logging.getLogger().setLevel(logging.DEBUG)

        pygame.init()
        self.screen = pygame.surface.Surface(SCREEN_SIZE)
        self.window = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(WINDOW_CAPTION)

        self.running = True
        self.clock = pygame.time.Clock()
        self.delta_time = 0.0

        self.world = load_ldtk(self.load_resource(WORLD_DATA_PATH))
        
        self._input_events = {}

        self.game_data = {}
        self.save_data = {}

        self.state = State(game_states)
        self.state.start(self,"init")

    def _quit(self):
        self.running = False

    def _update_clock(self):
        dt = self.clock.tick(FPS)/1000
        self.delta_time = dt

    def _draw_screen_to_window(self):
        pygame.transform.scale(self.get_screen(), pygame.display.get_window_size(), self.get_window()) 
    
    def _process_events(self):
        for input_event in self._input_events:
            if self._input_events[input_event] == RELEASED:
                self._input_events[input_event] = OFF
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key in input_events:
                key_name = input_events[event.key]
                if key_name in input_map:
                    self._input_events[input_map[key_name]] = PRESSED
            if event.type == pygame.KEYUP and event.key in input_events:
                key_name = input_events[event.key]
                if key_name in input_map:
                    self._input_events[input_map[key_name]] = RELEASED 

    def run(self):
        while self.running:
            self._process_events()
            self.state.process_events(self)
            self.state.update(self)
            self.state.draw(self)
            self._draw_screen_to_window()
            pygame.display.flip()
            self._update_clock()
        pygame.quit()
        logging.debug(f"program exited normally")
        sys.exit()
    
    def quit_game(self):
        self._quit()

    def get_delta_time(self):
        dt = self.delta_time
        return dt
    
    def get_screen(self):
        return self.screen
    
    def get_window(self):
        return self.window
    
    def load_resource(self, path):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)),path)
    
    def play_sound(self,filepath):
        if not os.path.exists(filepath):
            logging.debug(f"cannot play fx: fx filepath {filepath} does not exist")
            return
        sound = pygame.mixer.Sound(filepath)

        try:
            pygame.mixer.Sound.play(sound)
        except:
            logging.debug(f"could not play sounsound fx! here is the sound fx that was passed: {sound}")

    def play_music(self,filepath, volume=1.0, loop=-1):
        if not os.path.exists(filepath):
            logging.debug(f"cannot play music: music filepath {filepath} does not exist")
            return
        
        pygame.mixer.music.set_volume(volume)

        try:
            pygame.mixer.music.load(filepath)
        except:
            logging.error("could not load music!")
            return
        
        pygame.mixer.music.play(loop)
    
    def is_button_pressed(self, button_name, controller=None):
        if controller is None:
            if button_name in self._input_events:
                return True if self._input_events[button_name] == PRESSED else False
    
    def is_button_released(self, button_name, controller=None):
        if controller is None:
            if button_name in self._input_events:
                return True if self._input_events[button_name] == RELEASED else False

game_states = {
                "init" : init.Init,
                "splashscreen" : splashscreen.Splashscreen,
                "title_screen" : titlescreen.TitleScreen
                }
        