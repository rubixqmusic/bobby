
from src.state import State
from src.screens.titlescreen.resources import *

class MoneyInTransition(State):
    def on_state_enter(self, title_screen):
        self.title_screen = title_screen
        title_screen.overlay_transition.set_animation(MONEY_IN_ANIMATION)
        title_screen.overlay_transition.play()

        self.title_screen.overlay_transition.animation_finished.attach(self, "animation_finished")

    
    def update(self, title_screen):
        delta = title_screen.game.get_delta_time()
        title_screen.overlay_transition.update(delta)
    
    def draw(self, title_screen):
        title_screen.overlay_transition.draw()
    
    def animation_finished(self, animation):
        self.start_game_or_quit()

    def start_game_or_quit(self):
        self.title_screen.start_game_or_quit()
    
    def on_state_exit(self, title_screen):
        title_screen.overlay_transition.animation_finished.detach(self)

        
