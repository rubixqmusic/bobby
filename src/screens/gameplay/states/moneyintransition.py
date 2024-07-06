
from src.state import State
from src.screens.gameplay.resources import *

class MoneyInTransition(State):
    def on_state_enter(self, level):
        self.level = level
        level.transition_overlay.set_animation("money_in")
        level.transition_overlay.play()

        self.level.transition_overlay.animation_finished.attach(self, "animation_finished")

    
    def update(self, level):
        level.transition_overlay.update()
    
    def draw(self, level):
        level.transition_overlay.draw()
    
    def animation_finished(self, animation):
        self.start_scene()

    def start_scene(self):
        self.level.start_scene()
    
    def on_state_exit(self, level):
        level.transition_overlay.animation_finished.detach(self)

        
