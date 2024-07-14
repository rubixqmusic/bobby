from src.state import State
from src.bob import bob

from src.entities.bobby.resources import *

class Jumping(State):

    def update(self, bobby, delta):


        bobby.velocity.x = 0
        bobby.velocity.y = 0
        if bobby.is_on_ceiling():
            bobby.falling()
            return
        if bobby.jump_velocity < 0:
            bobby.falling()
            return
        
        bobby.velocity.y -= int(bobby.jump_velocity)


        if bob.is_button_pressed(RIGHT_BUTTON):
            bobby.velocity.x = bobby.speed
        elif bob.is_button_pressed(LEFT_BUTTON):
            bobby.velocity.x = -bobby.speed
        
        if not bob.is_button_pressed(ACTION_BUTTON_1):
            bobby.jump_velocity = 0
        
        if bobby.velocity.x > 0:
            bobby.direction = RIGHT
            bobby.sprite.set_animation(JUMPING_RIGHT)
        elif bobby.velocity.x < 0:
            bobby.direction = LEFT
            bobby.sprite.set_animation(JUMPING_LEFT)

        bobby.move(bobby.velocity.x, bobby.velocity.y)

        bobby.jump_velocity -= bobby.gravity