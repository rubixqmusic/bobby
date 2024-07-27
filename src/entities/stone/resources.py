from settings import *

SPRITESHEET = {
                "red_stone" : f"{GRAPHICS_PATH}/entities/red_stone.png",
                "blue_stone" : f"{GRAPHICS_PATH}/entities/blue_stone.png",
                "green_stone" : f"{GRAPHICS_PATH}/entities/green_stone.png"
}
STONE_VALUE = {
                "red_stone" : 10,
                "blue_stone" : 5,
                "green_stone" : 1
}

ANIMATION = f"{ANIMATIONS_PATH}/stone.json"
DEFAULT_INITIAL_STATE = f"idle"
COLLECTED_STATE = f"collected"
FLOATING_ANIMATION = f"idle"
COLLECTED_ANIMATION = f"collected"
STONE_SOUND = f"{SOUNDS_PATH}/coin.wav"

DEFAULT_STONE_TYPE = "green_stone"