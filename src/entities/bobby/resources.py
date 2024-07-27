from settings import*

CHARACTER_SPRITESHEET = f"{GRAPHICS_PATH}/entities/bobby.png"
CHARACTER_ANIMATION = f"{ANIMATIONS_PATH}/bobby.json"
COLLISION_TYPES = ["ground", "gold_coin", "silver_coin", "copper_coin", "green_stone", "blue_stone", "red_stone"]
SOLID_OBJECTS = ["ground"]
ITEMS = ["gold_coin", "silver_coin", "copper_coin", "green_stone", "blue_stone", "red_stone"]

JUMP_SOUND = f"{SOUNDS_PATH}/jump.wav"


RIGHT = "right"
LEFT = "left"

IDLE_STATE = "idle"
FALLING_STATE = "falling"
RUNNING_STATE = "running"
WALL_SLIDE_STATE = "wall_slide"
JUMPING_STATE = "jumping"
PIVOT_STATE = "pivot"

IDLE_RIGHT = "idle_right"
IDLE_LEFT = "idle_left"
FALLING_RIGHT = "fall_right"
FALLING_LEFT = "fall_left"
RUNNING_RIGHT = "run_right"
RUNNING_LEFT = "run_left"
WALL_SLIDE_RIGHT = "wall_slide_right"
WALL_SLIDE_LEFT = "wall_slide_left"
JUMPING_RIGHT = "jump_right"
JUMPING_LEFT = "jump_left"
PIVOT_RIGHT = "pivot_right"
PIVOT_LEFT = "pivot_left"

SPEED = 200
COYOTE_TIME =  6
JUMP_VELOCITY = 250
JUMP_TIME = 18
JUMP_HOLD = 2
EXTRA_JUMP_HOLD = 2
JUMP_RELEASE = 8

WALL_SLIDE_DELAY = 10

PIVOT_TIME = 6


DEBUG_HITBOX_COLOR = (255, 0, 0)
DEBUG_HITBOX_RANGE_COLOR = (200, 50, 25)