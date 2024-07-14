from src.state import State
from src.bob import bob

from src.entities.bobby.resources import *

class Jumping(State):

    def on_state_enter(self, bobby):
        self.jump_button_released = False
        self.wall_jump = True if bobby.velocity.x else False
        self.jump_hold = JUMP_HOLD
        # bobby.velocity.x = bobby.speed /2

    def on_state_exit(self, bobby):
        bobby.lock_x_during_jump = False
        
    def update(self, bobby, delta):
        # bobby.velocity.x = 0
        bobby.velocity.y = 0
        # if bobby.is_on_ceiling():
        #     bobby.falling()
        #     return
        if bobby.jump_time < 0 and self.jump_hold < 0:
            bobby.falling()
            return
        
        if self.wall_jump:
            velocity = int(bobby.jump_velocity * 0.75)
            bobby.velocity.y -= velocity
        else:
            bobby.velocity.y -= int(bobby.jump_velocity)

        if not self.wall_jump and not bobby.lock_x_during_jump:
 
            if bob.is_button_pressed(RIGHT_BUTTON):
                bobby.velocity.x = bobby.speed
            elif bob.is_button_pressed(LEFT_BUTTON):
                bobby.velocity.x = -bobby.speed
        
        if not bob.is_button_pressed(ACTION_BUTTON_1) and self.jump_button_released == False:
            self.jump_button_released = True
            bobby.jump_time = 5
        
        if bobby.velocity.x > 0:
            bobby.direction = RIGHT
            bobby.sprite.set_animation(JUMPING_RIGHT)
        elif bobby.velocity.x < 0:
            bobby.direction = LEFT
            bobby.sprite.set_animation(JUMPING_LEFT)

        bobby.move(bobby.velocity.x, bobby.velocity.y)

        bobby.jump_time -= 1

        if bobby.jump_time < 0:
            self.jump_hold -=1