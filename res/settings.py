import os

GAME_NAME = "BOBBY'S MONEY MADNESS"
WINDOW_CAPTION = "Bobby's Money Madness"
DEBUG_ENABLED = True

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

DEFAULT_FONT = "default3.otf"

SAVE_DATA_PATH = f"{os.path.expanduser('~')}/.bobby"

FILE_1_NAME = "file_1.json"
FILE_2_NAME = "file_2.json"
FILE_3_NAME = "file_3.json"

DEBUG_START_IN_STATE = "title_screen"

UP_BUTTON = "up_button"
DOWN_BUTTON = "down_button"
LEFT_BUTTON = "left_button"
RIGHT_BUTTON = "right_button"

START_BUTTON = "start_button"

ACTION_BUTTON_1 = "action_button_1"

GOLD_COLOR = "#FBCB1D"

WORLD_MAP_WIDTH = 320
WORLD_MAP_HEIGHT = 200
WORLD_MAP_DEFAULT_SCENE = "world_map_main"

ENTITIES_LAYER_NAME = "entities"
GROUND_1_LAYER_NAME = "ground_1"
GROUND_2_LAYER_NAME = "ground_2"
OVERLAY_1_LAYER_NAME = "overlay_1"