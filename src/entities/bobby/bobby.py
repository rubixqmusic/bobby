import pygame

from src.state import State
from src.entity import Entity
from src.signal import Signal
from src.entities.bobby.resources import *
from src.entities.bobby.entitystates import player_states

from src.components.animatedsprite import AnimatedSprite
from src.components.hitbox import Hitbox
from src.bob import bob

class Bobby(Entity):
    def __init__(self, starting_position, camera, gravity, draw_target, hitboxes) -> None:
        super().__init__()

        self.set_name("bobby")
        self.type = "bobby"
        self.jump_button_reset = True
        self.lock_x_during_jump = False
        self.direction = RIGHT
        self.jump_velocity = JUMP_VELOCITY
        self.jump_time = 0
        self.camera = camera
        self.speed = SPEED
        self.coyote_time = 0
        self.gravity = gravity
        self.generate_particles = Signal()
        self.position = pygame.Vector2(starting_position)
        self.velocity = pygame.Vector2([0,0])

        self.sprite = AnimatedSprite()
        self.sprite.load_spritesheet(bob.load_resource(CHARACTER_SPRITESHEET))
        self.sprite.load_animation(bob.load_resource(CHARACTER_ANIMATION))
        self.sprite.set_draw_target(draw_target)
        self.sprite.set_animation(IDLE_RIGHT)
        self.sprite.set_position(200,200)
        self.sprite.play()
        

        self.hitbox = Hitbox()
        self.hitbox._debug_show_range = True
        self.hitbox.set_type("bobby")
        self.hitbox.set_collision_types(COLLISION_TYPES)
        self.hitbox.set_colliders(hitboxes)
        self.hitbox.set_hitbox(0,0, 10,24)
        self.hitbox.set_offset(26,24)
        self.hitbox.set_position(self.position.x, self.position.y)
        

        self.camera.center(self.hitbox.get_hitbox().centerx, self.hitbox.get_hitbox().centery)

        self.state = State(player_states)

        self.set_animation(IDLE_RIGHT)

        self.idle()
        
    def update(self, delta):
        
        # if bob.is_button_pressed(ACTION_BUTTON_1):
        #     self.jump_button_reset = False
        if bob.is_button_released(ACTION_BUTTON_1):
            self.jump_button_reset = True

        self.state.update(self, delta)
        self.sprite.update(delta)
        self.hitbox.set_position(self.position.x, self.position.y)
        self.camera.center(self.hitbox.get_hitbox().centerx, self.hitbox.get_hitbox().centery)
    
    def draw(self):
        self.state.draw(self)
        self.sprite.set_position(self.position[0] - self.camera.x,self.position[1] - self.camera.y)
        self.sprite.draw()

        if DEBUG_ENABLED and DEBUG_SHOW_HITBOXES:
            pygame.draw.rect(self.camera.surface, DEBUG_HITBOX_COLOR, (self.hitbox.get_hitbox()[0] - self.camera.x, self.hitbox.get_hitbox()[1] - self.camera.y, self.hitbox.get_hitbox()[2], self.hitbox.get_hitbox()[3]), 1)
            if self.hitbox._debug_show_range:
                            hitbox_range = pygame.rect.Rect(0,0, self.hitbox._range, self.hitbox._range)
                            hitbox_range.center = self.hitbox._hitbox.center
                            pygame.draw.rect(self.camera.surface, DEBUG_HITBOX_RANGE_COLOR, (hitbox_range[0] - self.camera.x, hitbox_range[1] - self.camera.y, hitbox_range[2], hitbox_range[3]), 1)
# STATE TRANSITIONS

    def idle(self):
        if self.direction == RIGHT:
            self.set_animation(IDLE_RIGHT)
        elif self.direction == LEFT:
            self.set_animation(IDLE_LEFT)
        else:
            self.direction = RIGHT
            self.set_animation(IDLE_RIGHT)
        self.state.set_state(self, IDLE_STATE)

    def falling(self, coyote_time=0, x_velocity=0):
        if coyote_time:
            self.coyote_time = COYOTE_TIME
        else:
            self.coyote_time = 0

        self.velocity.x = x_velocity

        if self.direction == RIGHT:
            self.set_animation(FALLING_RIGHT)
        elif self.direction == LEFT:
            self.set_animation(FALLING_LEFT)
        else:
            self.direction = RIGHT
            self.set_animation(FALLING_RIGHT)
        self.state.set_state(self, FALLING_STATE)
    
    def running(self):
        self.state.set_state(self, RUNNING_STATE)

    def wall_slide(self):
        if self.direction == RIGHT:
            self.set_animation(WALL_SLIDE_RIGHT)
        elif self.direction == LEFT:
            self.set_animation(WALL_SLIDE_LEFT)
        self.state.set_state(self, WALL_SLIDE_STATE)

    def pivot(self):
        if self.direction == RIGHT:
            self.set_animation(PIVOT_RIGHT)
        elif self.direction == LEFT:
            self.set_animation(PIVOT_LEFT)
        # else:
        #     self.direction = RIGHT
        #     self.set_animation(PIVOT_RIGHT)
        self.state.set_state(self, PIVOT_STATE)

    def jumping(self, x_velocity=0, lock_x=False):
        self.jump_velocity = JUMP_VELOCITY
        self.jump_time = JUMP_TIME
        if not x_velocity:
            self.velocity.x = 0
        else:
            self.velocity.x = x_velocity
        
        if lock_x:
            self.lock_x_during_jump = True

        self.state.set_state(self, JUMPING_STATE)



    def move(self, x, y):
        current_state = self.state.get_name()

        if current_state == RUNNING_STATE:
            self.position.x += x
            self.hitbox.set_position(self.position.x, self.position.y - 1)
            collisions = self.hitbox.get_collisions()

            for collision in collisions:
                if collision.get_type() in SOLID_OBJECTS:
                    self.resolve_solid_collision_x(collision)
                elif collision.get_type() in ITEMS:
                    collision.on_collision.emit(self)
                    
            self.position.y += y
            self.hitbox.set_position(self.position.x, self.position.y - 1)
            collisions = self.hitbox.get_collisions()

            if collisions:
                for collision in collisions:
                    if collision.get_type() in SOLID_OBJECTS:
                        self.resolve_solid_collision_y(collision)
                    elif collision.get_type() in ITEMS:
                        collision.on_collision.emit(self)

        if current_state == PIVOT_STATE:
            self.position.x += x
            self.hitbox.set_position(self.position.x, self.position.y - 1)
            collisions = self.hitbox.get_collisions()

            for collision in collisions:
                if collision.get_type() in SOLID_OBJECTS:
                    self.resolve_solid_collision_x(collision)
                elif collision.get_type() in ITEMS:
                        collision.on_collision.emit(self)
                    
            self.position.y += y
            self.hitbox.set_position(self.position.x, self.position.y - 1)
            collisions = self.hitbox.get_collisions()

            if collisions:
                for collision in collisions:
                    if collision.get_type() in SOLID_OBJECTS:
                        self.resolve_solid_collision_y(collision)
                    elif collision.get_type() in ITEMS:
                        collision.on_collision.emit(self)
        

        if current_state == FALLING_STATE:
            self.position.x += x
            self.hitbox.set_position(self.position.x, self.position.y - 1)
            collisions = self.hitbox.get_collisions()

            if collisions:
                for collision in collisions:
                    if collision.get_type() in SOLID_OBJECTS:
                        self.resolve_solid_collision_x(collision)
                        self.wall_slide()
                        break
                    elif collision.get_type() in ITEMS:
                        collision.on_collision.emit(self)

            self.position.y += y
            self.hitbox.set_position(self.position.x, self.position.y - 1)
            collisions = self.hitbox.get_collisions()

            if collisions:
                for collision in collisions:
                    if collision.get_type() in SOLID_OBJECTS:
                        self.resolve_solid_collision_y(collision)
                    elif collision.get_type() in ITEMS:
                        collision.on_collision.emit(self)


        if current_state == WALL_SLIDE_STATE:
            self.position.x += x
            self.hitbox.set_position(self.position.x, self.position.y - 1)
            collisions = self.hitbox.get_collisions()
            
            if not collisions:
                self.falling()
            else:
                for collision in collisions:
                    if collision.get_type() in SOLID_OBJECTS:
                        self.resolve_solid_collision_x(collision)
                    elif collision.get_type() in ITEMS:
                        collision.on_collision.emit(self)
                    else:
                        self.falling()
            
            self.position.y += y
        

        if current_state == JUMPING_STATE:
            
            # print(x)

            self.position.x += x
            self.hitbox.set_position(self.position.x, self.position.y - 1)
            collisions = self.hitbox.get_collisions()

            for collision in collisions:
                if collision.get_type() in SOLID_OBJECTS:
                    self.resolve_solid_collision_x(collision)
                elif collision.get_type() in ITEMS:
                    collision.on_collision.emit(self)
                    # self.wall_slide()

            self.position.y += y
            self.hitbox.set_position(self.position.x, self.position.y - 1)
            collisions = self.hitbox.get_collisions()

            for collision in collisions:
                if collision.get_type() in SOLID_OBJECTS:

                    # print(collision.get_hitbox().top)
                    self.resolve_solid_collision_y(collision)
                    # self.position.y -= y
                    self.falling()
                    break
                elif collision.get_type() in ITEMS:
                    collision.on_collision.emit(self)




        # self.hitbox.set_position(self.position.x, self.position.y)
        # collisions = self.hitbox.get_collisions()
        # current_state = self.state.get_name()
        # if current_state == RUNNING_STATE:

        #     for collision in collisions:
        #         if collision.get_type() in SOLID_OBJECTS:
        #             self.resolve_solid_collision_y(collision)
        ...

    def set_animation(self, animation_name: str):
        self.sprite.set_animation(animation_name)


    def is_on_ground(self):
        self.hitbox.set_position(self.position.x, self.position.y + 1)
        collisions = self.hitbox.get_collisions()
        self.hitbox.set_position(self.position.x, self.position.y - 1)

        for collision in collisions:
            if collision.get_type() in SOLID_OBJECTS:
                return True
    
        return False
    
    def is_on_ceiling(self):
        self.hitbox.set_position(self.position.x, self.position.y - 3)
        collisions = self.hitbox.get_collisions()
        self.hitbox.set_position(self.position.x, self.position.y + 3)

        for collision in collisions:
            if collision.get_type() in SOLID_OBJECTS:
                if collision.get_hitbox()[1] < self.position.y:
                    return True
                  
        return False
    
    def resolve_solid_collision_y(self, hitbox):
        
        hitbox_previous_y = int(self.hitbox.get_hitbox()[1])

        if self.velocity.y > 0:            
            if self.hitbox.get_hitbox().bottom > hitbox.get_hitbox().top:
                
                self.hitbox.get_hitbox().bottom = hitbox.get_hitbox().top
                y_difference = hitbox_previous_y - self.hitbox.get_hitbox()[1]
                self.position.y -= y_difference
                self.position.y -= 1
                self.velocity.y = 0
                
        elif self.velocity.y < 0:
            if self.hitbox.get_hitbox().top < hitbox.get_hitbox().bottom:
                self.hitbox.get_hitbox().top = hitbox.get_hitbox().bottom
                y_difference = self.hitbox.get_hitbox()[1] - hitbox_previous_y
                self.position.y += y_difference
                self.position.y += 1
                self.velocity.y = 0
        else:
            pass
    
    def resolve_solid_collision_x(self, hitbox):
        hitbox_previous_x = int(self.hitbox.get_hitbox()[0])
        if self.velocity.x > 0:
            if self.hitbox.get_hitbox().right > hitbox.get_hitbox().left:
                self.hitbox.get_hitbox().right = hitbox.get_hitbox().left
                x_difference = hitbox_previous_x - self.hitbox.get_hitbox()[0]
                self.position.x -= x_difference
                self.position.x -= 1
                self.velocity.x = 0
        elif self.velocity.x < 0:
            if self.hitbox.get_hitbox().left < hitbox.get_hitbox().right:
                self.hitbox.get_hitbox().left = hitbox.get_hitbox().right
                x_difference = self.hitbox.get_hitbox()[0] - hitbox_previous_x
                self.position.x += x_difference
                self.position.x += 1
                self.velocity.x = 0
        
        
    