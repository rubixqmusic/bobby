import pygame

from src.state import State
from src.entity import Entity
from src.signal import Signal
from src.components.animatedsprite import AnimatedSprite
from src.components.hitbox import Hitbox
# from src.bob import bob

from src.entities.stone.resources import *
from src.entities.stone.entitystates import *
from src.signal import Signal
# from settings import *


class Stone(Entity):
    def __init__(self, level, coin_type=DEFAULT_STONE_TYPE) -> None:
        super().__init__()
        self.level = level
        self.type = coin_type
        self.value = STONE_VALUE[coin_type]
        self.camera = level.camera
        self.position = pygame.Vector2([0,0])
        self.velocity = pygame.Vector2([0,0])

        self.animated_sprite = AnimatedSprite()
        self.animated_sprite.load_spritesheet(level.game.load_resource(SPRITESHEET[coin_type]))
        self.animated_sprite.load_animation(level.game.load_resource(ANIMATION))
        self.animated_sprite.set_draw_target(self.camera.surface)
        self.animated_sprite.set_animation(FLOATING_ANIMATION)
        self.animated_sprite.set_position(0,0)
        self.animated_sprite.play()
        self.animated_sprite.animation_finished.attach(self, "on_animation_finished")

        self.hitbox = Hitbox()
        self.hitbox.set_type(DEFAULT_STONE_TYPE)
        self.hitbox.set_collision_types("bobby")
        self.hitbox.set_colliders(level.hitboxes)
        self.hitbox.set_hitbox(0,0,12,12)
        self.hitbox.set_offset(2,2)
        self.hitbox.set_position(self.position.x, self.position.y)
        self.hitbox.on_collision.attach(self, "hit")

        self.state = State(states)
        self.state.set_state(self, DEFAULT_INITIAL_STATE)

        self.idle()
    
    def set_position(self, position_x, position_y):
        self.position.x = position_x
        self.position.y = position_y
        self.hitbox.set_position(self.position.x, self.position.y)

    def hit(self, entity):
        if self.state.name == "idle" and entity.type == "bobby":
            self.hitbox.disable()
            self.state.set_state(self, COLLECTED_STATE)
            self.level.collect_coin(self)
            # self.collect_coin.emit(self)
    
    def on_animation_finished(self, animation):
        if animation == COLLECTED_ANIMATION:
            self.kill()
    
    def idle(self):
        self.state.set_state(self, DEFAULT_INITIAL_STATE)


    def update(self, delta):
        self.state.update(self, delta)
        self.animated_sprite.update(delta)
        self.hitbox.set_position(self.position.x, self.position.y)
    
    def draw(self):
        self.state.draw(self)
        self.animated_sprite.set_position(self.position[0] - self.camera.x,self.position[1] - self.camera.y)
        self.animated_sprite.draw()

        if DEBUG_ENABLED and DEBUG_SHOW_HITBOXES:
            pygame.draw.rect(self.camera.surface, (255,0,0), (self.hitbox.get_hitbox()[0] - self.camera.x, self.hitbox.get_hitbox()[1] - self.camera.y, self.hitbox.get_hitbox()[2], self.hitbox.get_hitbox()[3]), 1)

    def kill(self):
        self.hitbox._alive = False
        return super().kill()