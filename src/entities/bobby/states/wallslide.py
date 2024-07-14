from src.state import State
from src.bob import bob

from src.entities.bobby.resources import *

class WallSlide(State):
    def update(self, bobby, delta):
        bobby.velocity.x = 0
        bobby.velocity.y = 0
        if bobby.is_on_ground():
            bobby.idle()
            return
        else:
            bobby.velocity.y += int(bobby.gravity/2)
            
        if bob.is_button_pressed(RIGHT_BUTTON):
            bobby.velocity.x = bobby.speed
        elif bob.is_button_pressed(LEFT_BUTTON):
            bobby.velocity.x = -bobby.speed

        bobby.move(bobby.velocity.x, bobby.velocity.y)