from src.state import State
from src.screens.worldmap.resources import *

class MapActive(State):
    def update(self, world_map):
        if world_map.game.is_button_released(SELECT_BUTTON):
            world_map.quit_menu()