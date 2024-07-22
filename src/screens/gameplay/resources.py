from settings import *

TRANSITION_SPRITESHEET = f"{GRAPHICS_PATH}/screen_transitions/screen_transitions.png"
TRANSITION_ANIMATION = f"{ANIMATIONS_PATH}/screen_transitions.json"

PAUSE_MENU_IMAGE = f"{GRAPHICS_PATH}/text_box/text_box.png"

DEFAULT_LEVEL_MUSIC = f"{MUSIC_PATH}/main_level.mp3"

LEVEL_MUSIC = {
                "default" : f"{MUSIC_PATH}/main_level.mp3"
               }

MENU_OPEN_SOUND = f"{SOUNDS_PATH}/menu_open.wav"
MENU_CLOSE_SOUND = f"{SOUNDS_PATH}/menu_close.wav"
PAUSE_MENU_SELECT_SOUND = f"{SOUNDS_PATH}/menu_select.wav"
RETURN_TO_MAIN_MENU_SOUND = f"{SOUNDS_PATH}/return_to_main_menu.wav"

BACKGROUND_IMAGE_FILE_EXTENSION = f".png"

PAUSE_MENU_FONT_SIZE = 12
PAUSE_MENU_FONT_COLOR = GOLD_COLOR
PAUSE_MENU_FONT = f"{FONTS_PATH}/default3.otf"

MAX_TEXT_GROW = 5.0
TEXT_GROW_STEP_SIZE = 0.1

DEFAULT_GRAVITY = 230

LEVEL_TILESET_IDENTIFIER = "levels"

# entity identifiers

GOLD_COIN_ENTITY = "gold_coin"

HITBOX_TYPES = ["ground", "bobby", "gold_coin"]

MAX_ENTITIES = 1000
MAX_HITBOXES = 5000
MAX_PARTICLES = 3000

TILE_DATA = {
                "ground" :  {
                                "solid" : True,
                             }
}