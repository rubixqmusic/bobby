from settings import *

TRANSITION_SPRITESHEET = f"{GRAPHICS_PATH}/screen_transitions/screen_transitions.png"
TRANSITION_ANIMATION = f"{ANIMATIONS_PATH}/screen_transitions.json"

DEFAULT_LEVEL_MUSIC = f"{MUSIC_PATH}/main_level.mp3"

LEVEL_MUSIC = {
                "default" : f"{MUSIC_PATH}/main_level.mp3"
               }

BACKGROUND_IMAGE_FILE_EXTENSION = f".png"

DEFAULT_GRAVITY = 230

LEVEL_TILESET_IDENTIFIER = "levels"

HITBOX_TYPES = ["ground", "bobby"]

MAX_ENTITIES = 1000
MAX_HITBOXES = 5000
MAX_PARTICLES = 3000

TILE_DATA = {
                "ground" :  {
                                "solid" : True,
                             }
}