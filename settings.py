import os
import enum

GAME_NAME = "BOBBY'S MONEY MADNESS"
WINDOW_CAPTION = "Bobby's Money Madness"
EXECUTABLE_NAME = "Bobbys-Money-Maddness.appimage"

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 288
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 576
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT

DISPLAY_MODES = {
                    "fullscreen" : "fullscreen",
                    "mode_1" : (2048, 1152),
                    "mode_2" : (1024, 576),
                    "mode_3" : (512, 288)
                }

FPS = 60

RESOURCE_FILE_NAME = "bob.res"
RESOURCE_DIRS = [
                    "res/animations", 
                    "res/cutscenes",
                    "res/audio/fx", 
                    "res/audio/music", 
                    "res/fonts", 
                    "res/graphics/animated_tilesets", 
                    "res/graphics/backgrounds",
                    "res/graphics/entities", 
                    "res/graphics/hud", 
                    "res/graphics/icons",
                    "res/graphics/player",
                    "res/graphics/scene_backgrounds",
                    "res/graphics/scene_backgrounds/bg_1",
                    "res/graphics/scene_backgrounds/bg_2",
                    "res/graphics/scene_backgrounds/bg_3",
                    "res/graphics/scene_backgrounds/bg_image",
                    "res/graphics/screen_transitions",
                    "res/graphics/text_box",
                    "res/graphics/tilesets",
                    "res/graphics/video_call_cutscenes",
                    "res/graphics/world_map",
                    "res/tileset_animations"
                ]

FONTS_PATH = "res/fonts"
SOUNDS_PATH = "res/audio/fx"
MUSIC_PATH = "res/audio/music"
GRAPHICS_PATH = "res/graphics"
WORLD_DATA_PATH = "res/bobby.ldtk"
BASE_PATH = "res/"
ANIMATIONS_PATH = "res/animations"
TILESET_ANIMATIONS_PATH = "res/tileset_animations"

DEFAULT_FONT = "default3.otf"
DEFAULT_FONT_SIZE = 12

SAVE_DATA_FILE_NAME = "bob.sav"
SAVE_DATA_PATH = f"{os.path.expanduser('~')}/.bobby"

FILE_1_NAME = "file_1.json"
FILE_2_NAME = "file_2.json"
FILE_3_NAME = "file_3.json"

QUIT_KEY = "quit_key"
UP_BUTTON = "up_button"
DOWN_BUTTON = "down_button"
LEFT_BUTTON = "left_button"
RIGHT_BUTTON = "right_button"
START_BUTTON = "start_button"
SELECT_BUTTON = "select_button"
ACTION_BUTTON_1 = "action_button_1"
ACTION_BUTTON_2 = "action_button_2"
ACTION_BUTTON_3 = "action_button_3"
ACTION_BUTTON_4 = "action_button_4"

GOLD_COLOR = "#FBCB1D"

DEFAULT_TRANSITION = "money_in"

WORLD_MAP_WIDTH = 320
WORLD_MAP_HEIGHT = 200
WORLD_MAP_DEFAULT_SCENE = "world_map_main"

ENTITIES_LAYER_NAME = "entities"
GROUND_1_LAYER_NAME = "ground_1"
GROUND_2_LAYER_NAME = "ground_2"
MAIN_GROUND_LAYER_NAME = "main_ground"
OVERLAY_1_LAYER_NAME = "overlay_1"
OVERLAY_2_LAYER_NAME = "overlay_2"



# Debug settings ------------------------------------------------------------]

DEBUG_ENABLED = False
DEBUG_START_IN_STATE = "title_screen"
DEBUG_LEVEL_NAME = "sunset_beach"
DEBUG_LEVEL_START_POSITION = [185,466]
DEBUG_LEVEL_START_TRANSITION = "money_in"
DEBUG_VIDEO_CALL_CUTSCENE = "intro_1"