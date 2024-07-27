from src.state import State
from src.entities.coin.resources import *

class Idle(State):
    def on_state_enter(self, coin):
        coin.animated_sprite.set_animation(FLOATING_ANIMATION)

    def update(self, object, delta):
        ...