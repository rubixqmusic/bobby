from settings import *

SPRITESHEET = {
                "gold_coin" : f"{GRAPHICS_PATH}/entities/gold_coin.png",
                "silver_coin" : f"{GRAPHICS_PATH}/entities/silver_coin.png",
                "copper_coin" : f"{GRAPHICS_PATH}/entities/copper_coin.png"
}
COIN_VALUE = {
                "gold_coin" : 20,
                "silver_coin" : 5,
                "copper_coin" : 1
}

ANIMATION = f"{ANIMATIONS_PATH}/coin.json"
DEFAULT_INITIAL_STATE = f"idle"
COLLECTED_STATE = f"collected"
FLOATING_ANIMATION = f"idle"
COLLECTED_ANIMATION = f"collected"
COIN_SOUND = f"{SOUNDS_PATH}/coin.wav"

DEFAULT_COIN_TYPE = "gold_coin"