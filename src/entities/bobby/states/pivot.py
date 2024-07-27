from src.state import State
# from src.bob import bob

from src.entities.bobby.resources import *

class Pivot(State):
    def on_state_enter(self, bobby):
        self.pivot_time = PIVOT_TIME

    def update(self, bobby, delta):
        bobby.velocity.x = 0
        bobby.velocity.y = 0
        if bobby.is_on_ground():
            bobby.velocity.y = 0
        else:
            bobby.falling(True)
            return
        
        # if bob.is_button_pressed(RIGHT_BUTTON) and bobby.direction == RIGHT:
        #     bobby.running()
        #     return
        # if bob.is_button_pressed(LEFT_BUTTON) and bobby.direction == LEFT:
        #     bobby.running()
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
        
        if bobby.direction == LEFT:
            bobby.velocity.x = int(-SPEED * 0.5)
        elif bobby.direction == RIGHT:
            bobby.velocity.x = int(SPEED * 0.5)
        
        x = int(bobby.velocity.x * delta)
        y = int(bobby.velocity.y * delta)
        
        bobby.move(x, y)

        print(self.pivot_time)

        self.pivot_time -= 1

        if self.pivot_time <= 0:
            if bobby.direction == RIGHT:
                bobby.direction = LEFT
            if bobby.direction == LEFT:
                bobby.direction = RIGHT
            bobby.idle()
            return
        
