from src.state import State
from src.entities.coin.resources import *
# from src.bob import bob

class Collected(State):
    def on_state_enter(self, coin):
        # coin.level.game.play_sound(COIN_SOUND)
        coin.animated_sprite.set_animation(COLLECTED_ANIMATION)
    
    def update(self, object, delta):
        ...