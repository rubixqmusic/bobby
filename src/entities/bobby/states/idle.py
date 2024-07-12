from src.state import State
from src.bob import bob

from src.entities.bobby.resources import *

class Idle(State):
    def update(self, bobby, delta):
        bobby.velocity.x = 0

        if bob.is_button_pressed(RIGHT_BUTTON):
            bobby.velocity.x = bobby.speed
        elif bob.is_button_pressed(LEFT_BUTTON):
            bobby.velocity.x = -bobby.speed

        bobby.position.x += bobby.velocity.x
        bobby.camera.move(bobby.velocity.x, bobby.velocity.y)