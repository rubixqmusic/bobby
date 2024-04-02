import os
import enum

GAME_NAME = "BOBBY'S MONEY MADNESS"
WINDOW_CAPTION = "Bobby's Money Madness"

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 288
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 576
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT

FPS = 60

FONTS_PATH = "../fonts"
SOUNDS_PATH = "../audio/fx"
MUSIC_PATH = "../audio/music"
GRAPHICS_PATH = "../graphics"
WORLD_DATA_PATH = "../bobby.ldtk"
BASE_PATH = "../"
ANIMATIONS_PATH = "../animations"
TILESET_ANIMATIONS_PATH = "../tileset_animations"

DEFAULT_FONT = "default3.otf"

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
OVERLAY_1_LAYER_NAME = "overlay_1"



# Debug settings ------------------------------------------------------------]

DEBUG_ENABLED = True
DEBUG_START_IN_STATE = "playing_level"
DEBUG_LEVEL_NAME = "sunset_beach"
DEBUG_LEVEL_START_POSITION = [0,0]
DEBUG_LEVEL_START_TRANSITION = "money_in"
DEBUG_VIDEO_CALL_CUTSCENE = "intro_1"