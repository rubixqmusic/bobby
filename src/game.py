import pygame
import os
import sys
import logging
import json
import base64
import io
from datetime import datetime

from settings import *
from src.utilities.resourcemanager import *
from src.state import State
# from src.gamestates import init, splashscreen, titlescreen, fileselectscreen, videocallcutscene, worldmap, playinglevel
from src.screens.screens import screens
from res.input_events import *
from savedata import save_data

OFF = 0
PRESSED = 1
RELEASED = 2

class Game:
    def __init__(self) -> None:
        
        self._resource_pack = {}
        self._load_resource_pack()

        self.save_data_template = {}

        for key in save_data:
            self.save_data_template[key] = save_data[key]
            
        self.save_data = save_data
        
        self._save_file_database = {}
        self._load_save_file_database()

        if DEBUG_ENABLED == True:
            logging.getLogger().setLevel(logging.DEBUG)

        pygame.init()

        self.screen = pygame.surface.Surface(SCREEN_SIZE)
        display_info = pygame.display.Info()
        self.window = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(WINDOW_CAPTION)

        if not self._resource_pack:
            logging.error(f"no resource file could be found. womp womp. aborting this horseshit. fuck you")
            pygame.quit()
            sys.exit()

        pygame.display.set_icon(pygame.image.load(self.load_resource(f"{GRAPHICS_PATH}/icons/icon.png")))

        self.running = True
        self.clock = pygame.time.Clock()
        self.delta_time = 0.0
        self.world = None
        self.world = json.load(self.load_resource(WORLD_DATA_PATH))
        
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

        self.debug_font = pygame.font.Font(self.load_resource(f"{FONTS_PATH}/{DEFAULT_FONT}"), DEFAULT_FONT_SIZE)

        if not os.path.exists(SAVE_DATA_PATH):
            try:
                os.mkdir(SAVE_DATA_PATH)
            except:
                logging.debug(f"Could not create save data path {SAVE_DATA_PATH}, make sure you have proper privileges to create this file!")
        
        self.state = State(screens)
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
        if not self._resource_pack:
            logging.error(f"program exited in a fucked up manner. We couldn't find a resource pack. fuck you")
            pygame.quit()
            sys.exit()
        if self.world is None:
            logging.error(f"program exited in a fucked up manner. No world file could be loaded, fam, so we aborted that shit")
            pygame.quit()
            sys.exit()
        while self.running:
            self._iterate()
        pygame.quit()
        logging.debug(f"program exited normally")
        sys.exit()
    
    def _iterate(self):
        self._process_events()
        self.state.process_events(self)
        self.state.update(self)
        self.state.draw(self)
        if DEBUG_ENABLED:
            self._draw_debug()  
        self._draw_screen_to_window()
        pygame.display.flip()
        self._update_clock()
    
    def _draw_debug(self):
        camera_pos = [0,0]
        try:
            camera_pos[0] = self.state.camera.get_position()[0]
            camera_pos[1] = self.state.camera.get_position()[1]
        except AttributeError:
            pass

        debug_fps = self.debug_font.render(f"FPS: {int(self.get_fps())}", True, (255,255,255))
        debug_camera_pos = self.debug_font.render(f"Camera Pos: {camera_pos}", True, (255,255,255))

        self.get_screen().blit(debug_fps, (12, 12))
        self.get_screen().blit(debug_camera_pos, (12, 28))

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

    def load_settings_screen(self):
        self.state.set_state(self, "settings_screen")
    
    def load_world_map(self):
        self.state.set_state(self, "world_map")
    
    def load_level(self, level_name, player_start_position=[0,0], transition=DEFAULT_TRANSITION):
        self.state.set_state(self, "playing_level", level_name, player_start_position, transition)
    
    def set_current_save_file(self, filepath):
        self._current_save_file = filepath
    
    def get_current_save_file(self):
        return self._current_save_file
    
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
    

    def _load_save_file_database(self):
        if os.path.exists(SAVE_DATA_FILE_NAME):
            with open(SAVE_DATA_FILE_NAME) as save_file_database:
                # save_file_database_decoded = base64.b64decode(save_file_database.read())
                save_file_database_data = decode_resource_file_to_object(save_file_database)

                for key in save_file_database_data:
                    new_value = save_file_database_data[key]
                    self._save_file_database[key] = new_value
        else:
            save_file_names = [FILE_1_NAME, FILE_2_NAME, FILE_3_NAME]
            for filename in save_file_names:
                self._save_file_database[filename] = {}
                for key in self.save_data_template:
                    self._save_file_database[filename][key] = self.save_data_template[key]
            self._write_save_file_database()
    
    def _write_save_file_database(self):
        write_resource_file_to_disk(SAVE_DATA_FILE_NAME, self._save_file_database)
        # with open(SAVE_DATA_FILE_NAME, 'wb') as save_file:
        #     save_file.write(base64.b64encode(json.dumps(self._save_file_database).encode()))


    def _load_resource_pack(self):
        try:
            with open(RESOURCE_FILE_NAME) as resource_pack:
                resource_pack_data = decode_resource_file_to_object(resource_pack)
            
                for key in resource_pack_data:
                    self._resource_pack[key] = generate_decoded_resource(resource_pack_data, key)

        except FileNotFoundError:
            logging.error(f"uh oh! no resrouce file named {RESOURCE_FILE_NAME} could be found!")
    

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

        if self._current_save_file in self._save_file_database:
            for key in self.save_data:
                self._save_file_database[self._current_save_file][key] = self.save_data[key]
            
            # print(self._save_file_database[self._current_save_file])


            self._write_save_file_database()
        else:
            logging.error(f"could not write save file database to disk! make sure you have the correct permissions, or correct save file selected!")

        # try:
        #     with open(self._current_save_file, 'w') as save_file:
        #         json.dump(self.save_data, save_file)
        # except:
        #     logging.debug(f"could not save game to file!")
    

    def load_save_file(self, filepath):

        


        if filepath in self._save_file_database:
            for key in self._save_file_database[filepath]:
                self.save_data[key] = self._save_file_database[filepath][key]
        else:
            logging.error(f"no save file called {filepath}, could not load save file")

        # if os.path.exists(filepath):
        #     try:
        #         with open(filepath) as save_file:
        #             save_file_data = json.load(save_file)

        #             for key, value in save_file_data:
        #                 self.save_data[key] = value         
        #     except:
        #         logging.debug(f"could not load in save file {filepath}! someone made an oopsie goofer")
        # else:
        #     logging.debug(f"could not load save file, filepath {filepath} does not exist!")
    

    def create_new_save_file(self, filepath):
        if filepath in self._save_file_database:
            for key in self.save_data_template:
                self.save_data[key] = self.save_data_template[key]
                self._save_file_database[filepath][key] = self.save_data_template[key]
            self._write_save_file_database()
        else:
            for key in self.save_data_template:
                self.save_data[key] = self.save_data_template[key]
            logging.error(f"could not create new save file and write to disk!")

    def copy_save_file(self, source_file, destination_file):
        if source_file in self._save_file_database and destination_file in self._save_file_database:
            for key in self._save_file_database[source_file]:
                self._save_file_database[destination_file][key] = self._save_file_database[source_file][key]
            self._write_save_file_database()
        # try:
        #     with open(filepath, 'w') as fp:
        #         json.dump(self.save_data, fp)
        # except:
        #     logging.debug(f"could not save file!")


    def get_save_data(self, save_data):
        if save_data in self.save_data:
            return self.save_data[save_data]
        else:
            return None
    
    def set_save_data(self, key, value):
        self.save_data[key] = value
    
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

# game_states = {
#                 "init" : init.Init,
#                 "splashscreen" : splashscreen.Splashscreen,
#                 "title_screen" : titlescreen.TitleScreen,
#                 "file_select_screen" : fileselectscreen.FileSelectScreen,
#                 "video_call_cutscene" : videocallcutscene.VideoCallCutscene,
#                 "world_map" : worldmap.WorldMap,
#                 "playing_level" : playinglevel.PlayingLevel
#                 }
        