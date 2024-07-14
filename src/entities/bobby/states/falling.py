from src.state import State
from src.bob import bob

from src.entities.bobby.resources import *

class Falling(State):
    def update(self, bobby, delta):
        if bobby.coyote_time:
            bobby.coyote_time -= 1
        bobby.velocity.x = 0
        bobby.velocity.y = 0
        if bobby.is_on_ground():
            # bobby.position.y -= 1
            bobby.idle()
            return
        else:
            bobby.velocity.y += bobby.gravity
            
        if bob.is_button_pressed(RIGHT_BUTTON):
            bobby.velocity.x = int(bobby.speed)
        elif bob.is_button_pressed(LEFT_BUTTON):
            bobby.velocity.x = -int(bobby.speed)

        # bobby.position.y += bobby.velocity.y
        # bobby.position.x += bobby.velocity.x
        if bobby.velocity.x > 0:
            bobby.direction = RIGHT
            bobby.sprite.set_animation(FALLING_RIGHT)
        elif bobby.velocity.x < 0:
            bobby.direction = LEFT
            bobby.sprite.set_animation(FALLING_LEFT)

        bobby.move(bobby.velocity.x, bobby.velocity.y)
        # bobby.camera.move(bobby.velocity.x, bobby.velocity.y)