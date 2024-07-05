from settings import *
import pygame

class Bob:
    
    def init(self, game):
        self._game = game
    
    def load_resource(self, resource_path) -> None:
        return self._game.load_resource(resource_path)
        

    def play_sound(self, sound) -> None:
        self._game.play_sound(sound)

    def play_music(self, music, volume = 1.0, loop = -1) -> None:
        self._game.play_music(music, volume, loop)
    
    def stop_music(self) -> None:
        self._game.stop_music()
    
    def quit(self) -> None:
        self._game.quit_game()

    def get_delta_time(self):
        return self._game.get_delta_time()

    def get_screen(self) -> pygame.surface.Surface :
        return self._game.get_screen()
    
    def get_window(self) -> pygame.display :
        return self._game.get_window()
    
    def is_button_pressed(self, button, controller = 1) -> bool:
        return self._game.is_button_pressed(button, controller)
    
    def is_button_released(self, button, controller = 1) -> bool:
        return self._game.is_button_released(button, controller)

bob = Bob()