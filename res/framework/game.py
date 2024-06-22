import pygame
import os
import sys
import logging
import json
import base64
import io
from datetime import datetime

from res.settings import *
from res.utilities.ldtk_loader import load_ldtk
from res.framework.state import State
from res.framework.gamestates import init, splashscreen, titlescreen, fileselectscreen, videocallcutscene, worldmap, playinglevel
from res.input_events import *
from res.savedata import save_data

OFF = 0
PRESSED = 1
RELEASED = 2

class Game:
    def __init__(self) -> None:
        
        self._resource_pack = {}
        self._load_resource_pack()
        # print(f"\n\n {sys.platform} \n\n")
        # print(f"\n\n {os.path.expanduser('~')} \n\n")

        if DEBUG_ENABLED == True:
            logging.getLogger().setLevel(logging.DEBUG)

        pygame.init()
        self.screen = pygame.surface.Surface(SCREEN_SIZE)

        display_info = pygame.display.Info()
        self.window = pygame.display.set_mode(WINDOW_SIZE)
        # self.window = pygame.display.set_mode((display_info.current_w, display_info.current_h), pygame.FULLSCREEN)

        pygame.display.set_caption(WINDOW_CAPTION)
        pygame.display.set_icon(pygame.image.load(self.load_resource(f"{GRAPHICS_PATH}/icons/icon.png")))

        

        self.running = True
        self.clock = pygame.time.Clock()
        self.delta_time = 0.0

        # self.world = load_ldtk(self.load_resource(WORLD_DATA_PATH))
        

        self.world = None
        self.world = json.load(self.load_resource(WORLD_DATA_PATH))

        # try:
        #     with open(self.load_resource(WORLD_DATA_PATH)) as world_data:
        #         self.world = json.load(world_data)
        # except:
        #     logging.debug(f"FATAL ERROR: Could not load world data file, shit's fucked fam")
        
        # print(self.world["levels"])
        
        self._input_events = {}
        self._joystick_events = {}
        self._joysticks = {}
        self._joystick_ports = { 1: None,
                                 2: None
                                 }
        self._current_music = ""
        self._current_file_name = ""
        self._current_save_file = ""

        self.game_data = {}
        self.save_data = save_data

        self.debug_font = pygame.font.Font(self.load_resource(f"{FONTS_PATH}/{DEFAULT_FONT}"), DEFAULT_FONT_SIZE)

        if not os.path.exists(SAVE_DATA_PATH):
            try:
                os.mkdir(SAVE_DATA_PATH)
            except:
                logging.debug(f"Could not create save data path {SAVE_DATA_PATH}, make sure you have proper privileges to create this file!")
        

        self.state = State(game_states)
        self.state.start(self,"init")


    def _quit(self):
        self.running = False
        # pygame.quit()

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
                    if "left_button" in self._joystick_events[event.instance_id]:
                        if self._joystick_events[event.instance_id]["left_button"] == PRESSED:
                            self._joystick_events[event.instance_id]["left_button"] = RELEASED
                    if "right_button" in self._joystick_events[event.instance_id]:
                        if self._joystick_events[event.instance_id]["right_button"] == PRESSED:
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
            
            if self.is_button_released(QUIT_KEY):
                self.quit_game()

    def run(self):
        if self.world is None:
            logging.debug(f"program exited in a fucked up manner. No world file could be loaded, fam, so we aborted that shit")
            pygame.quit()
            sys.exit()
        while self.running:
            self._process_events()
            self.state.process_events(self)
            self.state.update(self)
            self.state.draw(self)
            self._draw_debug() if DEBUG_ENABLED else None
            self._draw_screen_to_window()
            pygame.display.flip()
            self._update_clock()
        pygame.quit()
        logging.debug(f"program exited normally")
        sys.exit()
    
    def _draw_debug(self):
        debug_fps = self.debug_font.render(f"FPS: {int(self.get_fps())}", True, (255,255,255))

        self.get_screen().blit(debug_fps, (400, 20))

    def get_fps(self):
        return self.clock.get_fps()
    
    def run_video_call_cutscene(self, cutscene_name):
        self.state.set_state(self,"video_call_cutscene", cutscene_name)
    
    def load_splashscreen(self):
        self.state.set_state(self, "splashscreen")
    
    def load_title_screen(self):
        self.state.set_state(self, "title_screen")
    
    def load_file_select_screen(self):
        self.state.set_state(self, "file_select_screen")
    
    def load_world_map(self):
        self.state.set_state(self, "world_map")
    
    def load_level(self, level_name, player_start_position=[0,0], transition=DEFAULT_TRANSITION):
        self.state.set_state(self, "playing_level", level_name, player_start_position, transition)
    
    def set_current_save_file(self, filepath):
        self._current_save_file = filepath
    
    def get_scene_and_starting_position_from_iid(self, level_iid, entrance_iid)->tuple:
        for level in self.get_levels_from_world():
            if level["iid"] == level_iid:
                for layer in level["layerInstances"]:
                    if layer["__identifier"] == ENTITIES_LAYER_NAME:
                        for entity in layer["entityInstances"]:
                            if entity["iid"] == entrance_iid:
                                return level["identifier"], entity["px"]

        return None
    
    def get_levels_from_world(self):
        return self.world["levels"]
    
    def load_tileset(self, image_path, tilesets):
        if image_path not in tilesets:
            if self.resource_exists(image_path):
                new_tileset_surface = pygame.image.load(self.load_resource(image_path)).convert_alpha()
                tilesets[image_path] = new_tileset_surface
            else:
                logging.debug(f"could not load tileset! image path {image_path} does not exist!")
        else:
            if self.resource_exists(image_path):
                new_tileset_surface = pygame.image.load(self.load_resource(image_path)).convert_alpha()
                tilesets[image_path] = new_tileset_surface
            else:
                logging.debug(f"could not load tileset! image path {image_path} does not exist!")
    
    def _load_resource_pack(self):

        with open(RESOURCE_FILE_NAME) as resource_pack:
            resource_pack_decoded = base64.b64decode(resource_pack.read())
            resource_pack_data = json.loads(resource_pack_decoded)
           
            for key in resource_pack_data:
                new_value = base64.b64decode(resource_pack_data[key])
                self._resource_pack[key] = new_value
    
    def resource_exists(self, resource_path: str) -> bool:
        return True if resource_path in self._resource_pack else False

            


    def save_game(self):
        # if os.path.exists(self._current_save_file):

        months = {
                    1: "Jan",
                    2: "Feb",
                    3: "Mar",
                    4: "Apr",
                    5: "May",
                    6: "Jun",
                    7: "Jul",
                    8: "Aug",
                    9: "Sep",
                    10: "Oct",
                    11: "Nov",
                    12: "Dec"

        }
        timestamp = datetime.today()
        month = months[timestamp.month]
        day = timestamp.day
        year = timestamp.year
        self.save_data["last_saved"] = f"{month} {day}, {year}"
        try:
            with open(self._current_save_file, 'w') as save_file:
                json.dump(self.save_data, save_file)
        except:
            logging.debug(f"could not save game to file!")
    

    def load_save_file(self, filepath):
        if os.path.exists(filepath):
            try:
                with open(filepath) as save_file:
                    save_file_data = json.load(save_file)

                    for key, value in save_file_data:
                        self.save_data[key] = value         
            except:
                logging.debug(f"could not load in save file {filepath}! someone made an oopsie goofer")
        else:
            logging.debug(f"could not load save file, filepath {filepath} does not exist!")
    

    def create_new_save_file(self, filepath):
        try:
            with open(filepath, 'w') as fp:
                json.dump(self.save_data, fp)
        except:
            logging.debug(f"could not save file!")


    def get_save_data(self, save_data):
        if save_data in self.save_data:
            return self.save_data[save_data]
        else:
            return None
    
    def get_level_data(self, level_name):
        if level_name in self.save_data["levels"]:
            return self.save_data["levels"][level_name]
        else:
            return None
    
    def set_level_data(self, level_name, field, value):
        if level_name in self.save_data["levels"]:
            if field in self.save_data["levels"][level_name]:
                self.save_data["levels"][level_name][field] = value

    def set_current_level(self, level_name):
        if "current_level" in self.save_data and level_name in self.save_data["levels"]:
            self.save_data["current_levle"] = level_name
            
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
        if path in self._resource_pack:
            return io.BytesIO(self._resource_pack[path])
        else:
            return None
    
    def play_sound(self,filepath):
        # if not os.path.exists(filepath):
        #     logging.debug(f"cannot play fx: fx filepath {filepath} does not exist")
        #     return
        if not self.resource_exists(filepath):
            return
        
        sound = pygame.mixer.Sound(self.load_resource(filepath))

        try:
            pygame.mixer.Sound.play(sound)
        except:
            logging.debug(f"could not play sounsound fx! here is the sound fx that was passed: {sound}")

    def play_music(self,filepath, volume=1.0, loop=-1):
        # if not os.path.exists(filepath):
        #     logging.debug(f"cannot play music: music filepath {filepath} does not exist")
        #     return
        
        if self._current_music == filepath:
            return
        
        if not self.resource_exists(filepath):
            return
        
        pygame.mixer.music.set_volume(volume)

        try:
            pygame.mixer.music.load(self.load_resource(filepath))
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
                "video_call_cutscene" : videocallcutscene.VideoCallCutscene,
                "world_map" : worldmap.WorldMap,
                "playing_level" : playinglevel.PlayingLevel
                }
        