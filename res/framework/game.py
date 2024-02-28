import pygame
import os
import sys
import logging

from res.settings import *
from res.utilities.ldtk_loader import load_ldtk
from res.framework.state import State
from res.framework.gamestates import init, splashscreen, titlescreen, fileselectscreen, videocallcutscene
from res.input_events import *

OFF = 0
PRESSED = 1
RELEASED = 2

class Game:
    def __init__(self) -> None:

        # print(f"\n\n {sys.platform} \n\n")
        # print(f"\n\n {os.path.expanduser('~')} \n\n")

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
        self._joystick_events = {}
        self._joysticks = {}
        self._joystick_ports = { 1: None,
                                 2: None
                                 }
        self._current_music = ""
        self._current_file_name = ""

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
        self._input_events["quit"] = False
        for input_event in self._input_events:
            if self._input_events[input_event] == RELEASED:
                self._input_events[input_event] = OFF

        for instance_id in self._joystick_events:
            for joystick_event in self._joystick_events[instance_id]:
                if self._joystick_events[instance_id][joystick_event] == RELEASED:
                    self._joystick_events[instance_id][joystick_event] = OFF
        
        # print(self._joystick_events)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self._input_events["quit"] = True

            if event.type == pygame.KEYDOWN and event.key in input_events:
                key_name = input_events[event.key]
                if key_name in input_map:
                    self._input_events[input_map[key_name]] = PRESSED
            if event.type == pygame.KEYUP and event.key in input_events:
                key_name = input_events[event.key]
                if key_name in input_map:
                    self._input_events[input_map[key_name]] = RELEASED
        
            if event.type == pygame.JOYBUTTONDOWN:
                if not event.instance_id in self._joystick_events:
                    self._joystick_events[event.instance_id] = {}
                if event.button in input_map["BUTTONS"]:
                    button_name = input_map["BUTTONS"][event.button]
                    self._joystick_events[event.instance_id][button_name] = PRESSED
                # print(event)
                # print(self._joystick_events)
            
            if event.type == pygame.JOYBUTTONUP:
                if not event.instance_id in self._joystick_events:
                    self._joystick_events[event.instance_id] = {}
                if event.button in input_map["BUTTONS"]:
                    button_name = input_map["BUTTONS"][event.button]
                    self._joystick_events[event.instance_id][button_name] = RELEASED
                # print(self._joystick_events)

            if event.type == pygame.JOYAXISMOTION:
                ...
                # print(event)
            
            if event.type == pygame.JOYHATMOTION:
                if not event.instance_id in self._joystick_events:
                    self._joystick_events[event.instance_id] = {}
                if event.value[0] == 0:
                    self._joystick_events[event.instance_id]["left_button"] = RELEASED
                    self._joystick_events[event.instance_id]["right_button"] = RELEASED
                if event.value[0] == 1:
                    self._joystick_events[event.instance_id]["right_button"] = PRESSED
                if event.value[0] == -1:
                    self._joystick_events[event.instance_id]["left_button"] = PRESSED

                if event.value[1] == 0:
                    if "up_button" in self._joystick_events[event.instance_id]:
                        if self._joystick_events[event.instance_id]["up_button"] == PRESSED:
                            self._joystick_events[event.instance_id]["up_button"] = RELEASED
                    if "down_button" in self._joystick_events[event.instance_id]:
                        if self._joystick_events[event.instance_id]["down_button"] == PRESSED:
                            self._joystick_events[event.instance_id]["down_button"] = RELEASED
                if event.value[1] == 1:
                    self._joystick_events[event.instance_id]["up_button"] = PRESSED
                if event.value[1] == -1:
                    self._joystick_events[event.instance_id]["down_button"] = PRESSED
                # print(event)

            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                self._joysticks[joy.get_instance_id()] = joy
                for joystick in self._joystick_ports:
                    if self._joystick_ports[joystick] == None:
                        self._joystick_ports[joystick] = joy.get_instance_id()
                        break

            if event.type == pygame.JOYDEVICEREMOVED:
                del self._joysticks[event.instance_id]
                for joystick in self._joystick_ports:
                    if self._joystick_ports[joystick] == event.instance_id:
                        self._joystick_ports[joystick] = None
                # if event.instance_id in self._joystick_ports:
                #     self._joystick_ports[event.instance_id] = None

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
    
    def run_video_call_cutscene(self, cutscene_name):
        self.state.set_state(self,"video_call_cutscene", cutscene_name)
    
    def set_current_save_file(self, file_name):
        self._current_file_name = file_name

    def game_should_quit(self):
        if "quit" in self._input_events:
            return True if self._input_events["quit"] == True else False
        return False
    
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
        
        if self._current_music == filepath:
            return
        
        pygame.mixer.music.set_volume(volume)

        try:
            pygame.mixer.music.load(filepath)
        except:
            logging.error("could not load music!")
            return
        
        pygame.mixer.music.play(loop)
        self._current_music = filepath
    
    def stop_music(self):
        pygame.mixer.music.stop()
        self._current_music = ""
    
    def is_button_pressed(self, button_name, controller=1):
        controller_active = self._joystick_ports[controller]
        if controller_active is None:
            if button_name in self._input_events:
                return True if self._input_events[button_name] == PRESSED else False
        else:
            controller_instance_id = self._joystick_ports[controller]
            if controller_instance_id in self._joystick_events:
                if button_name in self._joystick_events[controller_instance_id]:
                    return True if self._joystick_events[controller_instance_id][button_name] == PRESSED else False
    
    def is_button_released(self, button_name, controller=1):
        controller_active = self._joystick_ports[controller]
        if controller_active is None:
            if button_name in self._input_events:
                return True if self._input_events[button_name] == RELEASED else False
        else:
            controller_instance_id = self._joystick_ports[controller]
            if controller_instance_id in self._joystick_events:
                if button_name in self._joystick_events[controller_instance_id]:
                    return True if self._joystick_events[controller_instance_id][button_name] == RELEASED else False

game_states = {
                "init" : init.Init,
                "splashscreen" : splashscreen.Splashscreen,
                "title_screen" : titlescreen.TitleScreen,
                "file_select_screen" : fileselectscreen.FileSelectScreen,
                "video_call_cutscene" : videocallcutscene.VideoCallCutscene
                }
        