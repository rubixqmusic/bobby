from src.state import State
# from src.bob import bob

from src.entities.bobby.resources import *

class WallSlide(State):
    def on_state_enter(self, bobby):
        self.wall_slide_delay = WALL_SLIDE_DELAY
        self.is_on_wall = True

    def update(self, bobby, delta):
        if bobby.direction == RIGHT:
            bobby.level.generate_particles(ParticleType.DUST_PARTICLE, [bobby.position.x + 38, bobby.position.y + 29])
        if bobby.direction == LEFT:
            bobby.level.generate_particles(ParticleType.DUST_PARTICLE, [bobby.position.x + 24, bobby.position.y + 29])
        bobby.velocity.x = 0
        bobby.velocity.y = 0
        if bobby.is_on_ground():
            # bobby.set_position(bobby.position.x, bobby.position.y - 1)
            bobby.idle()
            return
        else:
            bobby.velocity.y += int(bobby.gravity * 0.25)

        if self.wall_slide_delay <= 0:
         
            if bobby.level.game.is_button_pressed(ACTION_BUTTON_1) and bobby.jump_button_reset:
                bobby.jump_button_reset = False
                if bobby.direction == RIGHT:
                    x = int(-SPEED * delta)
                    bobby.move(x,0)
                    bobby.jumping(-SPEED)
                    return
                
                elif bobby.direction == LEFT:
                    x = int(SPEED * delta)
                    bobby.move(x,0)
                    bobby.jumping(SPEED)
                    return
        
        if bobby.level.game.is_button_pressed(RIGHT_BUTTON):
                self.is_on_wall = False
              
                bobby.velocity.x = bobby.speed
            
        elif bobby.level.game.is_button_pressed(LEFT_BUTTON):
            
            self.is_on_wall = False
            bobby.velocity.x = -bobby.speed
        
            # if bob.is_button_pressed(RIGHT_BUTTON) and self.is_on_wall:
            #     self.is_on_wall = False
            #     bobby.move(-2,0)
            #     bobby.falling(x_velocity=-2)
            #     # bobby.velocity.x = bobby.speed
            #     return
            # elif bob.is_button_pressed(LEFT_BUTTON) and self.is_on_wall:
                
            #     self.is_on_wall = False
            #     bobby.move(10,0)
            #     bobby.falling(x_velocity=2)
            #     # bobby.velocity.x = -bobby.speed\
            #     return
        if bobby.velocity.x and bobby.velocity.y != 0:
            bobby.velocity.normalize()
        x = int(bobby.velocity.x * delta)
        y = int(bobby.velocity.y * delta)

        bobby.move(x, y)

        self.wall_slide_delay -= 1

        if self.wall_slide_delay <= 0:
            self.wall_slide_delay = 0