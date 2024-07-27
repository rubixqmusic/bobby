from src.state import State
# from src.bob import bob

from src.entities.bobby.resources import *

class Idle(State):
    def update(self, bobby, delta):
        bobby.velocity.x = 0
        bobby.velocity.y = 0
        if bobby.is_on_ground():
            bobby.velocity.y = 0
        else:
            bobby.falling()
            return

        if bobby.level.game.is_button_pressed(RIGHT_BUTTON) or bobby.level.game.is_button_pressed(LEFT_BUTTON):
            bobby.running()
            return
        
        if bobby.level.game.is_button_pressed(ACTION_BUTTON_1) and bobby.jump_button_reset:
            bobby.jump_button_reset = False
            bobby.jumping()
            return

        bobby.move(bobby.velocity.x, bobby.velocity.y)
