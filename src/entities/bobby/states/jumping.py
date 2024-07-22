from src.state import State
from src.bob import bob

from src.entities.bobby.resources import *

class Jumping(State):

    def on_state_enter(self, bobby):
        self.jump_button_released = False
        self.wall_jump = True if bobby.velocity.x else False
        self.jump_hold = JUMP_HOLD
        self.extra_hold = False
        bob.play_sound(JUMP_SOUND)

        bobby.generate_particles.emit(JUMP_PARTICLE, [bobby.position.x + 32, bobby.position.y + 47],{})
        # bobby.velocity.x = bobby.speed /2

    def on_state_exit(self, bobby):
        bobby.lock_x_during_jump = False
        
    def update(self, bobby, delta):

        bobby.velocity.y = 0
        if self.wall_jump and bobby.jump_time > 0:
            velocity = bobby.jump_velocity
            bobby.velocity.y -= velocity
        elif bobby.jump_time > 0:
            bobby.velocity.y -= int(bobby.jump_velocity)

        if not self.wall_jump and not bobby.lock_x_during_jump:
 
            if bob.is_button_pressed(RIGHT_BUTTON):
                bobby.velocity.x = int(bobby.speed * 0.75)
            elif bob.is_button_pressed(LEFT_BUTTON):
                bobby.velocity.x = int(-bobby.speed * 0.75)
        
        if not bob.is_button_pressed(ACTION_BUTTON_1) and self.jump_button_released == False:
            self.jump_button_released = True
            bobby.jump_time -= JUMP_RELEASE
        
        if bobby.velocity.x > 0:
            bobby.direction = RIGHT
            bobby.set_animation(JUMPING_RIGHT)
        elif bobby.velocity.x < 0:
            bobby.direction = LEFT
            bobby.set_animation(JUMPING_LEFT)

        if bobby.jump_time < 0 and self.jump_hold < 0:
            bobby.falling(x_velocity=bobby.velocity.x)
            return

        if bobby.velocity.x and bobby.velocity.y != 0:
            bobby.velocity.normalize()

        x = int(bobby.velocity.x * delta)
        y = int(bobby.velocity.y * delta)

        bobby.move(x, y)

        bobby.jump_time -= 1

        if bobby.jump_time < 0:
            if bob.is_button_pressed(ACTION_BUTTON_1) and self.extra_hold == False:
                self.extra_hold = True
                self.jump_hold += EXTRA_JUMP_HOLD
            self.jump_hold -=1