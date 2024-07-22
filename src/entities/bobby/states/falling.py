from src.state import State
from src.bob import bob

from src.entities.bobby.resources import *

class Falling(State):
    def on_state_enter(self, bobby):
        self.lock_x_velocity = 0

        if bobby.velocity.x:
            self.lock_x_velocity = bobby.velocity.x

        self.jumping_into_wall = False
        
        if bobby.coyote_time == -1:
            self.jumping_into_wall = True


    def update(self, bobby, delta):
        if bobby.coyote_time:
            bobby.coyote_time -= 1
        if bobby.coyote_time <= 0:
            bobby.coyote_time = 0
        bobby.velocity.x = self.lock_x_velocity
        bobby.velocity.y = 0
        if bobby.is_on_ground():
            # bobby.position.y -= 1
            bobby.idle()
            return
        else:
            bobby.velocity.y += bobby.gravity
        
        if bob.is_button_pressed(ACTION_BUTTON_1) and bobby.coyote_time > 0 and bobby.jump_button_reset:
            bobby.jumping()

        # if self.lock_x_velocity:
        #     bobby.velocity.x = self.lock_x_velocity
        # elif not self.jumping_into_wall: 
        if not self.jumping_into_wall:

            if bob.is_button_pressed(RIGHT_BUTTON):
                bobby.velocity.x = int(bobby.speed)
            elif bob.is_button_pressed(LEFT_BUTTON):
                bobby.velocity.x = -int(bobby.speed)

        # bobby.position.y += bobby.velocity.y
        # bobby.position.x += bobby.velocity.x
        if bobby.velocity.x > 0:
            bobby.direction = RIGHT
            bobby.set_animation(FALLING_RIGHT)
        elif bobby.velocity.x < 0:
            bobby.direction = LEFT
            bobby.set_animation(FALLING_LEFT)

        if bobby.velocity.x and bobby.velocity.y != 0:
            bobby.velocity.normalize()
            
        x = int(bobby.velocity.x * delta)
        y = int(bobby.velocity.y * delta)

        bobby.move(x, y)
        # bobby.camera.move(bobby.velocity.x, bobby.velocity.y)