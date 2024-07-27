from src.state import State
# from src.bob import bob

from src.entities.bobby.resources import *

class Running(State):
    def update(self, bobby, delta):
        previous_x_velocity = bobby.velocity.x
        previous_y_velocity = bobby.velocity.y
        bobby.velocity.x = 0
        bobby.velocity.y = 0
        if bobby.is_on_ground():
            bobby.velocity.y = 0
        else:
            bobby.falling(True)
            return
        
        if bobby.level.game.is_button_pressed(RIGHT_BUTTON):
            bobby.velocity.x += bobby.speed
        elif bobby.level.game.is_button_pressed(LEFT_BUTTON):
            bobby.velocity.x -= bobby.speed
        else:
            bobby.idle()
            return
        
        # if bob.is_button_pressed(RIGHT_BUTTON) and previous_x_velocity < 0:
        #     bobby.pivot()
        #     return
        # if bob.is_button_pressed(LEFT_BUTTON) and previous_x_velocity > 0:
        #     bobby.pivot()
        #     return

        
        if bobby.level.game.is_button_pressed(ACTION_BUTTON_1) and bobby.jump_button_reset:
            bobby.jump_button_reset = False
            
            bobby.hitbox.set_position(bobby.position.x + 1, bobby.position.y -1)
            collisions = bobby.hitbox.get_collisions()

            if collisions:
                for collision in collisions:
                    if collision.get_type() in SOLID_OBJECTS:
                        bobby.resolve_solid_collision_x(collision)

                        bobby.jumping(lock_x=True)
                        
                        return
                    else:
                        bobby.jumping()
            else:
                bobby.jumping()
            return
        
        if bobby.velocity.x > 0:
            bobby.direction = RIGHT
            bobby.set_animation(RUNNING_RIGHT)
        elif bobby.velocity.x < 0:
            bobby.direction = LEFT
            bobby.set_animation(RUNNING_LEFT)

        if bobby.velocity.x and bobby.velocity.y != 0:
            bobby.velocity.normalize()
        x = int(bobby.velocity.x * delta)
        y = int(bobby.velocity.y * delta)
        
        bobby.move(x, y)