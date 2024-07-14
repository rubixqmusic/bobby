from src.state import State
from src.bob import bob

from src.entities.bobby.resources import *

class Running(State):
    def update(self, bobby, delta):
        bobby.velocity.x = 0
        bobby.velocity.y = 0
        if bobby.is_on_ground():
            bobby.velocity.y = 0
        else:
            bobby.falling()
            return
        
        if bob.is_button_pressed(ACTION_BUTTON_1):
            bobby.jumping()
            return
        
        if bob.is_button_pressed(RIGHT_BUTTON):
            bobby.velocity.x += bobby.speed
        elif bob.is_button_pressed(LEFT_BUTTON):
            bobby.velocity.x -= bobby.speed
        else:
            bobby.idle()
            return
        
        if bobby.velocity.x > 0:
            bobby.direction = RIGHT
            bobby.sprite.set_animation(RUNNING_RIGHT)
        elif bobby.velocity.x < 0:
            bobby.direction = LEFT
            bobby.sprite.set_animation(RUNNING_LEFT)
        
        bobby.move(bobby.velocity.x, bobby.velocity.y)