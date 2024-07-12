import pygame

from src.state import State
from src.entity import Entity
from src.entities.bobby.resources import *
from src.entities.bobby.entitystates import player_states

from src.components.animatedsprite import AnimatedSprite
from src.components.hitbox import Hitbox
from src.bob import bob

class Bobby(Entity):
    def __init__(self, starting_position, camera, gravity, draw_target, hitboxes) -> None:
        super().__init__()

        self.set_name("bobby")
        self.camera = camera
        self.speed = 3
        self.gravity = gravity
        self.position = pygame.Vector2(starting_position)
        self.velocity = pygame.Vector2([0,0])

        self.sprite = AnimatedSprite()
        self.sprite.load_spritesheet(bob.load_resource(CHARACTER_SPRITESHEET))
        self.sprite.load_animation(bob.load_resource(CHARACTER_ANIMATION))
        self.sprite.set_draw_target(draw_target)
        self.sprite.set_animation("idle_right")
        self.sprite.set_position(200,200)
        self.sprite.play()
        

        self.hitbox = Hitbox()
        self.hitbox.set_type("bobby")
        self.hitbox.set_collision_types(COLLISION_TYPES)
        self.hitbox.set_colliders(hitboxes)
        self.hitbox.set_hitbox(0,0, 10,24)
        self.hitbox.set_offset(26,24)
        self.hitbox.set_position(self.position.x, self.position.y)

        # self.hitbox.on_collision.attach(self, "on_collision")

        self.state = State(player_states)
        self.state.set_state(self, "idle")

    def update(self, delta):
        self.state.update(self, delta)
        self.sprite.update(delta)
        self.hitbox.set_position(self.position.x, self.position.y)
    
    def draw(self):
        self.state.draw(self)
        self.sprite.set_position(self.position[0] - self.camera.x,self.position[1] - self.camera.y)
        self.sprite.draw()

        pygame.draw.rect(self.camera.surface, (255,0,0), (self.hitbox.get_hitbox()[0] - self.camera.x, self.hitbox.get_hitbox()[1] - self.camera.y, self.hitbox.get_hitbox()[2], self.hitbox.get_hitbox()[3]), 1)

    